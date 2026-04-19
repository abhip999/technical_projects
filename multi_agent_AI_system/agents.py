from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from prompts import PLANNER_PROMPT, WRITER_PROMPT, REVIEWER_PROMPT
from config.config import GROQ_API_KEY, MODEL_NAME
llm = ChatGroq(
    temperature=0.7,
    model=MODEL_NAME,
    groq_api_key=GROQ_API_KEY
)

def planner_agent(topic):
    prompt = PromptTemplate.from_template(PLANNER_PROMPT)
    chain = prompt | llm
    return chain.invoke({"topic": topic}).content


def writer_agent(outline):
    prompt = PromptTemplate.from_template(WRITER_PROMPT)
    chain = prompt | llm
    return chain.invoke({"outline": outline}).content


def reviewer_agent(report):
    prompt = PromptTemplate.from_template(REVIEWER_PROMPT)
    chain = prompt | llm
    return chain.invoke({"report": report}).content


def generate_report(topic):
    outline = planner_agent(topic)
    draft = writer_agent(outline)
    final = reviewer_agent(draft)

    return {
        "outline": outline,
        "draft": draft,
        "final": final
    }