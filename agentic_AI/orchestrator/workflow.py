from agents.planner import create_plan
from agents.researcher import build_research_agent, research
from agents.writer import write_answer
from agents.reviewer import review


def run_multi_agent_system(query):
    # Step 1: Planning
    plan = create_plan(query)

    # Step 2: Research Loop
    research_agent = build_research_agent()
    research_outputs = []

    for step in plan.split("\n"):
        if step.strip():
            result = research(research_agent, step)
            research_outputs.append(result)

    combined_research = "\n".join(research_outputs)

    # Step 3: Writing
    draft = write_answer(query, combined_research)

    # Step 4: Review
    final_answer = review(draft)

    return {
        "plan": plan,
        "research": combined_research,
        "final": final_answer
    }