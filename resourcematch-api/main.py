from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import AnyHttpUrl, BaseModel
from typing import List, Literal
import json
import aiohttp
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


async def generate_search_queries(openai_client, model, text):
    content = (
        "Given an input from a user, please provide a set of no more than "
        "3 search phrases that would be appropriate to retrieve related "
        "content from a search engine. Each phrase should be 3 words or less. "
        "Return the response as a JSON string where the object has a key "
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


@app.post("/match")
async def perform_match(match_request: MatchRequest) -> MatchResponse:
    # TODO: Implement handler

    return MatchResponse(
        urls=[]
    )
