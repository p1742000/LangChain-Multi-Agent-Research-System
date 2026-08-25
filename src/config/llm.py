import os

from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI


def get_llm():

    provider = os.getenv("LLM_PROVIDER", "ollama").lower()

    if provider == "ollama":

        return ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "qwen3:4b"),
            temperature=0,
        )

    if provider == "openai":

        return ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY"),
        )

    if provider == "gemini":

        return ChatGoogleGenerativeAI(
            model=os.getenv("GEMINI_MODEL"),
            temperature=0,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )

    raise ValueError(
        f"Unsupported LLM provider: {provider}"
    )