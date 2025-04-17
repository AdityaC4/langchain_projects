from dotenv import load_dotenv
import os

load_dotenv()

from backend.core import run_llm
import streamlit as st

st.header("LangChain Documentation Helper")

prompt = st.text_input("Prompt", placeholder="Enter your prompt here...")

if "user_prompt_history" not in st.session_state:
    st.session_state.user_prompt_history = []

if "chat_answer_history" not in st.session_state:
    st.session_state.chat_answer_history = []

def create_sources_string(sources_urls: set[str]):
    if not sources_urls:
        return ""
    sources_list = list(sources_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i + 1}. {source}\n"
    return sources_string


if prompt:
    with st.spinner("Thinking..."):
        generated_response = run_llm(prompt)
        sources = set(
            [doc.metadata["source"] for doc in generated_response["source_documents"]]
        )

        formatted_response = (
            f"{generated_response['result']}\n\n {create_sources_string(sources)}"
        )

        st.session_state.user_prompt_history.append(prompt)
        st.session_state.chat_answer_history.append(formatted_response)

if st.session_state.user_prompt_history:
    for generated_response, user_query in zip(
        st.session_state.chat_answer_history,
        st.session_state.user_prompt_history,
    ):
        st.chat_message("user").write(user_query)
        st.chat_message("assistant").write(generated_response)
    
