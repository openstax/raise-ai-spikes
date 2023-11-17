from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import AnyHttpUrl, BaseModel
from typing import List, Literal
import aiohttp
import asyncio

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
    books_by_slug = {
        "college-algebra-corequisite-support-2e": {
            "uuid": "32bee6a",
            "code_version": "20230828.164620",
            "book_version": "59024a63-2b1a-4631-94c5-ae275a77b587"
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

    async with aiohttp.ClientSession() as session:
        first_book_slug = books[0]
        book_data = books_by_slug[first_book_slug]
        previously_used_queries = {}
        aggregate_search_results = []

        for query in search_queries:
            if query in previously_used_queries:
                continue
            previously_used_queries[query] = True
            url = (f'https://openstax.org/open-search/'
                   f'api/v0/search?q={query}'
                   f'&books={book_data['code_version']}/{book_data['uuid']}'
                   f'@{book_data['book_version']}'
                   f'&index_strategy=i1&search_strategy=s1')
            try:
                async with session.get(url) as resp:
                    resp.raise_for_status()
                    if resp.status == 200:
                        search_response = await resp.json()
                        search_info = {
                            "book": first_book_slug,
                            "search_query": query,
                            "search_response": search_response
                        }
                        aggregate_search_results.append(search_info)
            except aiohttp.ClientResponseError as exception:
                status = exception.status
                message = exception.message
                url = exception.args[0].url
                print({
                    'status': status,
                    'message': message,
                    'url': url
                })
        return aggregate_search_results


@app.post("/match")
async def perform_match(match_request: MatchRequest) -> MatchResponse:
    # TODO: Implement handler

    return MatchResponse(
        urls=[]
    )
