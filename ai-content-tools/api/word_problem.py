from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field


base_llm = ChatOpenAI(model="gpt-4o-mini")

PROMPT_TEMPLATE = """
You are math teacher. Given some math content and a problem type, generate a word problem where a student must work through steps to answer the problem. Provide a step by step solution as part of your word problem.

<content>
{content}
</content>
<problem_type>
{problem_type}
</problem_type>
"""


class WordProblem(BaseModel):
    word_problem: str = Field(description="generated math word problem")
    solution_work: str = Field(description="solution with steps to math word problem")


default_llm = base_llm.with_structured_output(WordProblem)

prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)

chain = prompt | default_llm
