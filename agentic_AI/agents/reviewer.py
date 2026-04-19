from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def review(answer):
    prompt = f"""
    Improve the answer for clarity, correctness, and completeness.

    Answer:
    {answer}
    """
    return llm.invoke(prompt).content