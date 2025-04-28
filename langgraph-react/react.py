from dotenv import load_dotenv
from langchain.agents import create_react_agent
from langchain import hub
from langchain_tavily import TavilySearch
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()

react_prompt: PromptTemplate = hub.pull("hwchase17/react")


@tool
def triple(num: float) -> float:
    """
    :param num: a number to triple
    :return: the number tripled -> multiplied by 3
    """
    return float(num) * 3


tools = [TavilySearch(max_results=1), triple]
llm = ChatOpenAI()

react_agent_runnable = create_react_agent(llm, tools, react_prompt)


if __name__ == "__main__":
    print(TavilySearch(max_results=1).invoke("what is the weather if sf?"))
