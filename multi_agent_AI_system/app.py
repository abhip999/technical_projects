import streamlit as st
from agents import generate_report

st.set_page_config(page_title="Multi-Agent Report Generator", layout="wide")

st.title("🧠 Multi-Agent AI Report Generator")

topic = st.text_input("Enter your topic")

if st.button("Generate Report"):
    if topic:
        with st.spinner("Agents are collaborating..."):
            result = generate_report(topic)

        st.success("Report Generated!")

        tab1, tab2, tab3 = st.tabs(["📌 Outline", "✍️ Draft", "✅ Final Report"])

        with tab1:
            st.markdown(result["outline"])

        with tab2:
            st.markdown(result["draft"])

        with tab3:
            st.markdown(result["final"])
    else:
        st.warning("Please enter a topic")