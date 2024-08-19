from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel
import rag
import word_problem
import similar_problem
from store import opensearch_vectorstore


app = FastAPI(
    title="Content Tools API",
)


class Reference(BaseModel):
    url: str
    title: str


class RAGInput(BaseModel):
    input: str


class WordProblem(BaseModel):
    equation: str
    scenario: str
    question: str
    answer: str
    work: str


class WordProblemInput(BaseModel):
    input: str


class WordProblemOutput(BaseModel):
    equation: str
    scenario: str
    question: str
    answer: str
    work: str


class RAGOutput(BaseModel):
    output: str
    references: List[Reference]


class SimilarProblemInput(BaseModel):
    input: str
    use_concepts: bool


class SimilarProblemOutput(BaseModel):
    similar_problem: str
    solution: str
    solution_work: str
    concepts: Optional[str]


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


@app.post("/word-problem")
def invoke_word_problem(data: WordProblemInput) -> WordProblemOutput:
    problem = word_problem.chain.invoke({"problem": data.input})

    return WordProblemOutput(
        equation=problem.equation,
        scenario=problem.scenario,
        question=problem.question,
        answer=problem.answer,
        work=problem.work,
    )


@app.post("/similar-problem")
def invoke_similar_problem(data: SimilarProblemInput) -> SimilarProblemOutput:

    if not data.use_concepts:
        problem = similar_problem.default_chain.invoke({"problem": data.input})

        return SimilarProblemOutput(
            similar_problem=problem.similar_problem,
            solution=problem.solution,
            solution_work=problem.solution_work,
            concepts=None,
        )

    concepts = similar_problem.concepts_chain.invoke({"problem": data.input})

    problem_from_concepts = similar_problem.problem_from_concepts_chain.invoke(
        {
            "problem": data.input,
            "concepts": concepts.math_concepts,
        }
    )

    return SimilarProblemOutput(
        similar_problem=problem_from_concepts.problem,
        solution=problem_from_concepts.solution,
        solution_work=problem_from_concepts.solution_work,
        concepts=concepts.math_concepts,
    )
