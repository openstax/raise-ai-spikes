from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field


base_llm = ChatOpenAI(model="gpt-4o-mini")

DEFAULT_PROMPT_TEMPLATE = """
You are math content developer. Given a math problem, generate a similar problem where a student must demonstrate the same understanding, but would have a different answer. Provide an answer and solution as part of your similar problem.

<problem>
{problem}
</problem>
"""


class SimilarProblem(BaseModel):
    """A math problem"""

    similar_problem: str = Field(description="generated similar math problem")
    solution: str = Field(description="solution to the generated similar math problem")
    solution_work: str = Field(description="worked solution to math problem")


default_llm = base_llm.with_structured_output(SimilarProblem)

default_prompt = PromptTemplate.from_template(DEFAULT_PROMPT_TEMPLATE)

default_chain = default_prompt | default_llm


CONCEPTS_PROMPT_TEMPLATE = """
You are math subject matter expert. Given a math problem, identify the key math concepts a student would be expected to know and exercise in order to solve it.

<problem>
{problem}
</problem>
"""


class ProblemConcepts(BaseModel):
    """Math concepts required to solve a math problem"""

    math_concepts: str = Field(
        description="concepts required to solve both math problems"
    )


problem_concepts_llm = base_llm.with_structured_output(ProblemConcepts)

concepts_prompt = PromptTemplate.from_template(CONCEPTS_PROMPT_TEMPLATE)

concepts_chain = concepts_prompt | problem_concepts_llm

PROBLEM_FROM_CONCEPTS_PROMPT_TEMPLATE = """
You are math content developer. Given a set of math concepts and an illustrative problem, generate a new problem where a student must demonstrate understanding of the same concepts. Provide an answer and solution as part of your new problem.

<concepts>
{concepts}
</concepts>

<problem>
{problem}
</problem>
"""


class ProblemFromConcepts(BaseModel):
    """A math problem"""

    problem: str = Field(description="generated math problem")
    solution: str = Field(description="solution to the generated math problem")
    solution_work: str = Field(description="worked solution to generated math problem")


problem_from_concepts_llm = base_llm.with_structured_output(ProblemFromConcepts)

problem_from_concepts_prompt = PromptTemplate.from_template(
    PROBLEM_FROM_CONCEPTS_PROMPT_TEMPLATE
)

problem_from_concepts_chain = problem_from_concepts_prompt | problem_from_concepts_llm
