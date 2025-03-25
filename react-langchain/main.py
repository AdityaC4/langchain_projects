from dotenv import load_dotenv

load_dotenv()


def get_text_length(text: str) -> int:
    """Returns the length of a test by characters"""
    return len(text)


if __name__ == "__main__":
    print("Hello ReAct LangChain!")
