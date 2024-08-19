from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

llm = ChatOpenAI(model="gpt-4o-mini")

PROMPT_TEMPLATE = """
"You are a writing assistant for teachers.
Given a math equation and a topic, you should provide a word problem that incorporates the math equation and the topic.
First work out your solution to the equation before providing the answer.
Do not provide an answer that is different from the work.
Do not include a question in the scenario."

<problem>
{problem}
<problem>
"""


class WordProblem(BaseModel):
    equation: str = Field(description="The equation submitted by the user.")
    scenario: str = Field(
        description="The word problem generated from a topic and an equation"
    )
    question: str = Field(
        description="The question for the student to answer based on the scenario"
    )
    work: str = Field(description="The work used to produce the answer")
    answer: str = Field(description="The answer generated from the work")


structured_output_llm = llm.with_structured_output(WordProblem)

prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)

chain = prompt | structured_output_llm
