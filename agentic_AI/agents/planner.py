from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def create_plan(query):
    prompt = f"""
    Break the user query into a step-by-step plan.

    Query: {query}

    Output format:
    1. Step 1
    2. Step 2
    3. Step 3
    """
    return llm.invoke(prompt).content