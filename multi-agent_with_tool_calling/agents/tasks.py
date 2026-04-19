from crewai import Task

def create_tasks(goal, planner, researcher, writer, critic):
    return [
        Task(description=f"Break goal into steps: {goal}", agent=planner),
        Task(description="Do research using tools", agent=researcher),
        Task(description="Write structured output", agent=writer),
        Task(description="Review and improve output", agent=critic),
    ]