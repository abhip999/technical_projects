from langchain_community.tools import DuckDuckGoSearchRun

def get_ddg_tool():
    return DuckDuckGoSearchRun()