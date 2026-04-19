import streamlit as st
from orchestrator.workflow import run_multi_agent_system

st.set_page_config(page_title="Multi-Agent AI System", layout="wide")

st.title("🤖 AutoGPT-style Multi-Agent System")

query = st.text_input("Enter your query")

if st.button("Run System"):
    if query:
        with st.spinner("Running multi-agent workflow..."):
            result = run_multi_agent_system(query)

        st.subheader("🧠 Plan")
        st.write(result["plan"])

        st.subheader("🔍 Research")
        st.write(result["research"])

        st.subheader("✅ Final Answer")
        st.write(result["final"])
    else:
        st.warning("Enter a query")