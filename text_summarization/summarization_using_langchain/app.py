import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain


load_dotenv()

# Initialize LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

map_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
    Summarize the following text concisely while preserving key information 
    and reduce the length of text by approximately 70 percent but don't tell the user about the reduction.
    Here is the text to summarize:

    {text}
    """
)

combine_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
    Combine the following summaries into a final structured summary:

    {text}
    """
)

def summarize_document(text):
    # Step 1: Split text into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )

    docs = splitter.create_documents([text])

    # Step 2: Load summarization chain (map_reduce)
    chain = load_summarize_chain(
        llm=llm,
        chain_type="map_reduce",
        map_prompt=map_prompt,
        combine_prompt=combine_prompt
    )

    # Step 3: Run summarization
    summary = chain.run(docs)

    return summary


st.title("📄 LLM Text Summarizer (LangChain + Groq)")

text = st.text_area("Enter your text")

if st.button("Summarize"):
    if text:
        with st.spinner("Summarizing..."):
            summary = summarize_document(text)
        st.write(summary)