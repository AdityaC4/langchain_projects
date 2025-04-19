from dotenv import load_dotenv
import os

load_dotenv()

from backend.core import run_llm
import streamlit as st

# Custom CSS for fonts and extra theme tweaks
st.markdown(
    """
    <style>
    html, body, [class*="css"]  {
        font-family: 'Georgia', serif !important;
        background-color: #FCF8EF !important;
    }
    .stButton>button {
        background-color: #7A9A3F !important;
        color: #fff !important;
        border-radius: 8px !important;
        border: none !important;
    }
    .stSidebar {
        background-color: #F5EEDC !important;
    }
    .stChatMessage, .stTextInput, .stTextArea, .stMarkdown, .stHeader {
        color: #4B463C !important;
    }
    /* Custom chat bubbles */
    .chat-bubble {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 16px;
        max-width: 70%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        font-size: 1.05rem;
        line-height: 1.5;
        word-break: break-word;
    }
    .user-bubble {
        background-color: #fff;
        margin-left: auto;
        border: 1px solid #e6e6e6;
    }
    .assistant-bubble {
        background-color: #F5EEDC;
        margin-right: auto;
        border: 1px solid #e6e6e6;
    }
    .chat-row {
        display: flex;
        align-items: flex-end;
    }
    .avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        margin: 0 8px;
        object-fit: cover;
        border: 1px solid #e6e6e6;
        background: #fff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar with user info
with st.sidebar:
    st.image("https://randomuser.me/api/portraits/men/32.jpg", width=100)  # Replace with actual profile pic URL or path
    st.markdown("**Name:** John Doe")
    st.markdown("**Email:** johndoe@example.com")

st.header("LangChain Documentation Helper")

prompt = st.text_input("Prompt", placeholder="Enter your prompt here...")

if (
    "chat_answer_history" not in st.session_state
    and "user_prompt_history" not in st.session_state
    and "chat_history" not in st.session_state
):
    st.session_state.user_prompt_history = []
    st.session_state.chat_answer_history = []
    st.session_state.chat_history = []

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
        generated_response = run_llm(prompt, st.session_state.chat_history)
        sources = set(
            [doc.metadata["source"] for doc in generated_response["source_documents"]]
        )

        formatted_response = (
            f"{generated_response['result']}\n\n {create_sources_string(sources)}"
        )

        st.session_state.user_prompt_history.append(prompt)
        st.session_state.chat_answer_history.append(formatted_response)
        st.session_state.chat_history.append(("human", prompt))
        st.session_state.chat_history.append(("ai", generated_response["result"]))

if st.session_state.user_prompt_history:
    for generated_response, user_query in zip(
        st.session_state.chat_answer_history,
        st.session_state.user_prompt_history,
    ):
        st.markdown(
            f'''
            <div class="chat-row" style="justify-content: flex-end;">
                <div class="chat-bubble user-bubble">{user_query}</div>
                <img src="https://randomuser.me/api/portraits/men/32.jpg" class="avatar"/>
            </div>
            <div class="chat-row" style="justify-content: flex-start;">
                <img src="https://cdn-icons-png.flaticon.com/512/4712/4712035.png" class="avatar"/>
                <div class="chat-bubble assistant-bubble">{generated_response}</div>
            </div>
            ''',
            unsafe_allow_html=True
        )
