import streamlit as st
from app.summarizer import summarize_document

st.set_page_config(page_title="LLM Text Summarizer")

st.title("📄 LLM Text Summarizer")

input_text = st.text_area("Enter your text here:")

if st.button("Summarize"):
    if input_text.strip():
        with st.spinner("Generating summary..."):
            summary = summarize_document(input_text)
        st.subheader("Summary:")
        st.write(summary)
    else:
        st.warning("Please enter some text.")