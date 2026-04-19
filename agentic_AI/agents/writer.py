from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

def write_answer(query, research_data):
    prompt = f"""
    Use the research below to answer the query.

    Query:
    {query}

    Research:
    {research_data}

    Provide a clear, structured answer.
    """
    return llm.invoke(prompt).content