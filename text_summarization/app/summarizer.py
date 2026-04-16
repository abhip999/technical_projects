from groq import Groq
from config.config import GROQ_API_KEY, MODEL_NAME
from app.utils import chunk_text

client = Groq(api_key=GROQ_API_KEY)

def summarize_chunk(chunk):
    prompt = f"""
    Summarize the following text concisely while preserving key information 
    and reduce the length of text by approximately 70% but don't tell the user about the reduction
    ,if possible try to provide it in some bullet points format. Here is the text to summarize:

    {chunk}
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def summarize_document(text):
    chunks = chunk_text(text)
    summaries = []

    for chunk in chunks:
        summaries.append(summarize_chunk(chunk))

    combined_summary = " ".join(summaries)

    # refinement step
    final_summary = summarize_chunk(combined_summary)

    return final_summary