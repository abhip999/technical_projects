import streamlit as st
from agents.crew import run_crew

st.set_page_config(page_title="Agentic AI", layout="wide")

st.title("🤖 Multi-Agent AI System")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Enter your goal..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🤖 Agents working..."):
            response = run_crew(prompt)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})