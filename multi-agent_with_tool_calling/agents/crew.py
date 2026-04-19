import os
from crewai import Crew, Process, Agent, Task
from .agents import create_agents
from config.config import llm_llama
from crewai.tools import BaseTool

# =========================
# 🔧 CUSTOM TOOLS (COMPATIBLE)
# =========================

class SearchTool(BaseTool):
    name: str = "Search Internet"
    description: str = "Search the internet for recent information"

    def _run(self, query: str) -> str:
        try:
            from duckduckgo_search import DDGS
            results = DDGS().text(query, max_results=5)
            return str(list(results))
        except Exception as e:
            return f"Search error: {str(e)}"


class WikipediaTool(BaseTool):
    name: str = "Wikipedia Lookup"
    description: str = "Get factual information from Wikipedia"

    def _run(self, query: str) -> str:
        try:
            import wikipedia
            return wikipedia.summary(query, sentences=5)
        except Exception as e:
            return f"Wikipedia error: {str(e)}"


class ArxivTool(BaseTool):
    name: str = "Arxiv Research"
    description: str = "Search research papers from Arxiv"

    def _run(self, query: str) -> str:
        try:
            import arxiv
            search = arxiv.Search(
                query=query,
                max_results=3,
                sort_by=arxiv.SortCriterion.Relevance
            )
            results = []
            for paper in search.results():
                results.append({
                    "title": paper.title,
                    "summary": paper.summary[:300],
                    "link": paper.entry_id
                })
            return str(results)
        except Exception as e:
            return f"Arxiv error: {str(e)}"

tools = [
    SearchTool(),
    WikipediaTool(),
    ArxivTool()
]

# =========================
# 📋 TASKS
# =========================

def create_tasks(goal, planner, researcher, writer, critic):

    planning_task = Task(
        description=f"""
        Break this goal into clear step-by-step actions:
        {goal}
        """,
        expected_output="Structured step-by-step plan",
        agent=planner
    )

    research_task = Task(
        description="""
        Use available tools (Search, Wikipedia, Arxiv) to gather
        detailed and accurate information based on the plan.
        """,
        expected_output="Detailed research insights",
        agent=researcher
    )

    writing_task = Task(
        description="""
        Convert the research into a structured report with headings,
        bullet points, and clear explanations.
        """,
        expected_output="Well-structured report",
        agent=writer
    )

    review_task = Task(
        description="""
        Review the report for clarity, accuracy, and completeness.
        Improve wherever necessary.
        """,
        expected_output="Final improved report",
        agent=critic
    )

    return [planning_task, research_task, writing_task, review_task]


# =========================
# 🚀 RUN CREW
# =========================

def run_crew(goal: str):

    planner, researcher, writer, critic = create_agents(llm_llama, tools)
    tasks = create_tasks(goal, planner, researcher, writer, critic)

    crew = Crew(
        agents=[planner, researcher, writer, critic],
        tasks=tasks,
        process=Process.sequential,
        memory=False,
        verbose=True
    )

    try:
        result = crew.kickoff()
        return result
    except Exception as e:
        return f"❌ Error: {str(e)}"