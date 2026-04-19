from langchain_community.tools import ArxivQueryRun
from langchain_community.utilities import ArxivAPIWrapper

def get_arxiv_tool():
    api_wrapper = ArxivAPIWrapper(top_k_results=3, doc_content_chars_max=500)
    return ArxivQueryRun(api_wrapper=api_wrapper)