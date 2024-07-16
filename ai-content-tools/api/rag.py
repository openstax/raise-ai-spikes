from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

PROMPT_TEMPLATE = """
You are a writing assistant for teachers. Given a prompt consisting of a question or topic and context, you should provide one or two paragraphs that a teacher can incorporate directly into their lesson plans.

<prompt>
{prompt}
</prompt>

<context>
{context}
</context>
"""


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def start(data):
    return {
        "context": format_docs(data["docs"]),
        "prompt": data["input"],
    }


llm = ChatOpenAI(model="gpt-3.5-turbo")

prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)

chain = RunnableLambda(start) | prompt | llm | StrOutputParser()
