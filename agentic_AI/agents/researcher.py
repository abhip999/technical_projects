from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI

from tools.wiki_tool import get_wikipedia_tool
from tools.arxiv_tool import get_arxiv_tool
from tools.ddg_tool import get_ddg_tool


def build_research_agent():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    tools = [
        get_wikipedia_tool(),
        get_arxiv_tool(),
        get_ddg_tool()
    ]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=False
    )

    return agent


def research(agent, step):
    return agent.run(step)