from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import AnyHttpUrl, BaseModel
from typing import List, Literal
import aiohttp
import logging

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
    model: Literal["gpt-3.5-turbo", "gpt-4"]
    books: List[Literal[
        "college-algebra-corequisite-support-2e",
        "world-history-volume-2",
        "us-history",
        "biology-2e"
    ]]
    text: str


class MatchResponse(BaseModel):
    urls: List[AnyHttpUrl]


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


async def search_responses_to_urls(search_responses):
    # Loop through the search_responses to obtain book information and the list of hits
    async with aiohttp.ClientSession() as session:
        ordered_urls = []
        for response in search_responses:
            book_data = BOOKS_BY_SLUG[response['book']]
            book_uuid = book_data['uuid']
            search_query = response['search_query']
            response_hits = response['search_response']['hits']['hits']
            # Loop through each hit to get the information necessary to make GET request
            for hit in response_hits:
                search_score = hit['_score']
                page_uuid = hit['_source']['page_id']
                fixed_page_uuid = page_uuid.partition('@')[0]
                element_uuid = hit['_source']['element_id']
                # Make GET request for each hit and return the URL associated with the applicable hit
                async with session.get(f"https://orn.openstax.org/orn/book:page/{book_uuid}:{fixed_page_uuid}.json") as resp:
                    page_data = await resp.json()
                    page_url_main = page_data['urls']['main']
                    appended_url = f"{page_url_main}#{element_uuid}"
                    search_query_with_url = {
                        "search_score": search_score,
                        "search_query": search_query,
                        "url": appended_url
                    }
                    ordered_urls.append(search_query_with_url)

        sorted_list = sorted(ordered_urls, key=lambda search_data: search_data['search_query'])
        return sorted_list


@app.post("/match")
async def perform_match(match_request: MatchRequest) -> MatchResponse:
    # TODO: Implement handler

    return MatchResponse(
        urls=[]
    )
