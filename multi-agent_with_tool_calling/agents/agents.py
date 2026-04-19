from crewai import Agent

def create_agents(llm, tools):

    planner = Agent(
        role="Strategic Planner",
        goal="Break down goals into structured steps",
        backstory="Expert in planning and task decomposition",
        llm=llm,
        verbose=True
    )

    researcher = Agent(
        role="Researcher",
        goal="Find accurate and relevant information",
        backstory="Expert in web and academic research using tools",
        tools=tools,
        llm=llm,
        verbose=True
    )

    writer = Agent(
        role="Writer",
        goal="Generate structured and clear content",
        backstory="Professional content writer",
        llm=llm,
        verbose=True
    )

    critic = Agent(
        role="Critic",
        goal="Improve quality and correctness",
        backstory="Strict reviewer ensuring high-quality output",
        llm=llm,
        verbose=True
    )

    return planner, researcher, writer, critic