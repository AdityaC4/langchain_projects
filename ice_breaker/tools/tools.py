from langchain_community.tools.tavily_search import TavilySearchResults


def get_profile_uyl_tavily(name: str):
    search = TavilySearchResults()
    res = search.run(f"{name}")
    return res
