from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from third_parties import scrape_linkedin_profile
from agents import lookup as linkedin_lookup_agent

def ice_breaker_with(name: str) -> str:
    linkedin_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url, mock=True)

    summary_template = """
        given the LinkedIn information {information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_varaiables=["information"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

    chain = summary_prompt_template | llm

    res = chain.invoke(input={"information": linkedin_data})

    print(res)

if __name__ == "__main__":
    print("Ice Breaker Enter")
    ice_breaker_with(name="Aditya Chaudhari ICER")
