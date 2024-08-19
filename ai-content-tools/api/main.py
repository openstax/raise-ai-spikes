from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import rag
import content_word_problem
from store import opensearch_vectorstore


app = FastAPI(
    title="Content Tools API",
)


class Reference(BaseModel):
    url: str
    title: str


class RAGInput(BaseModel):
    input: str


class RAGOutput(BaseModel):
    output: str
    references: List[Reference]


class ContentWordProblemInput(BaseModel):
    input: str
    problem_type: str


class ContentWordProblemOutput(BaseModel):
    content_word_problem: str
    solution_work: str


@app.post("/rag")
def invoke_rag(data: RAGInput) -> RAGOutput:
    docs = opensearch_vectorstore.similarity_search(data.input)

    output = rag.chain.invoke({"docs": docs, "input": data.input})

    references = []

    urls = set()

    for doc in docs:
        doc_url = doc.metadata["url"]
        if doc_url not in urls:
            references.append(
                {
                    "url": doc_url,
                    "title": doc.metadata["title"],
                }
            )
            urls.add(doc_url)

    return RAGOutput(
        output=output,
        references=references,
    )


@app.post("/content-word-problem")
def invoke_content_word_problem(data: ContentWordProblemInput) -> ContentWordProblemOutput:

    problem = content_word_problem.chain.invoke({"content": data.input,
                                                 "problem_type": data.problem_type})

    return ContentWordProblemOutput(
        content_word_problem=problem.content_word_problem,
        solution_work=problem.solution_work,
    )
