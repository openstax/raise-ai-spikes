from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import AnyHttpUrl, BaseModel
from typing import List, Literal
import json
import aiohttp
from requests import get
from functools import cache
import logging
from openai import OpenAI

client = OpenAI()

logger = logging.getLogger(__name__)


BOOKS_BY_SLUG = {
        "college-algebra-corequisite-support-2e": {
            "uuid": "59024a63-2b1a-4631-94c5-ae275a77b587",
            "code_version": "20230828.164620",
            "book_version": "32bee6a"
        },
        "world-history-volume-2": {
            "uuid": "685e3163-1032-4529-bb3a-f97a54412704",
            "code_version": "20230828.164620",
            "book_version": "244d248"
        },
        "us-history": {
            "uuid": "a7ba2fb8-8925-4987-b182-5f4429d48daa",
            "code_version": "20230828.164620",
            "book_version": "59e152a"
        },

        "biology-2e": {
            "uuid": "8d50a0af-948b-4204-a71d-4826cba765b8",
            "code_version": "20230828.164620",
            "book_version": "3bf8607"
        }
    }
SEARCH_API_BASE_URL = "https://openstax.org/open-search/api/v0"


app = FastAPI(
    title="Resource Match API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"]
)


class MatchRequest(BaseModel):
    model: Literal["gpt-3.5-turbo-1106", "gpt-4-1106"]
    books: List[Literal[
        "college-algebra-corequisite-support-2e",
        "world-history-volume-2",
        "us-history",
        "biology-2e"
    ]]
    text: str


class MatchResponse(BaseModel):
    urls: List[AnyHttpUrl]


async def generate_search_queries(openai_client, model, text):
    content = (
        "Given an input from a user, please provide a set of no more than "
        "3 search phrases that would be appropriate to retrieve related "
        "content from a search engine. Each search phrase has to be 3 words "
        "or less. Please confirm that every search term in the list is less "
        "than 4 words. Return the response as JSON where the object has a key "
        "'search_queries' with an array of selected terms."
    )

    chat_completion = openai_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": content,
            },
            {
                "role": "user",
                "content": text
            }
        ],
        model=model,
        max_tokens=512,
        response_format={"type": "json_object"},
        temperature=1.0
    )
    result = json.loads(chat_completion.choices[0].message.content)
    return result['search_queries']


async def process_search_queries(search_queries, books):
    async with aiohttp.ClientSession() as session:
        first_book_slug = books[0]
        book_data = BOOKS_BY_SLUG[first_book_slug]
        unique_search_queries = set(search_queries)
        aggregate_search_results = []

        for query in unique_search_queries:
            params = {
                "q": query,
                "books": (f"{book_data['code_version']}/{book_data['uuid']}"
                          f"@{book_data['book_version']}"),
                "index_strategy": "i1",
                "search_strategy": "s1"
            }
            try:
                async with session.get(
                        f"{SEARCH_API_BASE_URL}/search",
                        params=params) as resp:
                    resp.raise_for_status()
                    search_response = await resp.json()
                    search_info = {
                        "book": first_book_slug,
                        "search_query": query,
                        "search_response": search_response
                    }
                    aggregate_search_results.append(search_info)
            except aiohttp.ClientResponseError as exception:
                logger.error(
                    'Error processing request: %s',
                    exception,
                    exc_info=True)

        return aggregate_search_results


def search_responses_to_urls(search_responses):
    unsorted_hits = []
    sorted_hit_urls = []

    for response in search_responses:
        book_data = BOOKS_BY_SLUG[response['book']]
        book_uuid = book_data['uuid']
        search_query = response['search_query']
        response_hits = response['search_response']['hits']['hits']
        for hit in response_hits:
            search_score = hit['_score']
            element_uuid = hit['_source']['element_id']
            page_uuid = hit['_source']['page_id']
            page_uuid_partition = page_uuid.partition('@')[0]
            page_data = get_book_page_data(book_uuid, page_uuid_partition)
            page_url_main = page_data['urls']['main']
            appended_url_element_id = f"{page_url_main}#{element_uuid}"
            hit_data = {
                "hit_score": search_score,
                "hit_query": search_query,
                "hit_url": appended_url_element_id
            }
            unsorted_hits.append(hit_data)

    hits_sorted_by_hit_query = sorted(unsorted_hits,
                                      key=lambda
                                      hit_data: hit_data['hit_query'])
    for hit in hits_sorted_by_hit_query:
        sorted_hit_urls.append(hit['hit_url'])
    return sorted_hit_urls


@cache
def get_book_page_data(book_uuid, partitioned_page_uuid):
    url = (f"https://orn.openstax.org/orn/"
           f"book:page/{book_uuid}:{partitioned_page_uuid}.json")
    response = get(url)
    return response.json()


@app.post("/match")
async def perform_match(match_request: MatchRequest) -> MatchResponse:
    model = match_request.model
    text = match_request.text
    books = match_request.books
    search_queries = await generate_search_queries(client, model, text)
    search_responses = await process_search_queries(search_queries, books)
    sorted_urls = search_responses_to_urls(search_responses)

    return MatchResponse(
        urls=sorted_urls
    )
