from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import AnyHttpUrl, BaseModel
from typing import List, Literal
import json
from openai import OpenAI
client = OpenAI()

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


@app.post("/match")
async def perform_match(match_request: MatchRequest) -> MatchResponse:
    # TODO: Implement handler

    return MatchResponse(
        urls=[]
    )
