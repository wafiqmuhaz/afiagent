from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Optional

from src.config import (
    REASONING_MODEL,
    REASONING_API_KEY,
    BASIC_MODEL,
    BASIC_API_KEY,
    VL_MODEL,
    VL_API_KEY,
)
from src.config.agents import LLMType
from src.crawler.llm_client import LLMClient

# Initialize the LLMClient for local model access
local_llm_client = LLMClient()

def create_gemini_llm(
    model: str,
    api_key: Optional[str] = None,
    temperature: float = 0.0,
    **kwargs,
) -> ChatGoogleGenerativeAI:
    """
    Create a ChatGoogleGenerativeAI instance with the specified configuration
    """
    llm_kwargs = {"model": model, "temperature": temperature, **kwargs}

    if api_key:  # This will handle None or empty string
        llm_kwargs["google_api_key"] = api_key

    return ChatGoogleGenerativeAI(**llm_kwargs)


# Cache for LLM instances
_llm_cache: dict[LLMType, ChatGoogleGenerativeAI] = {}


def get_llm_by_type(llm_type: LLMType, use_local_model: bool = False) -> ChatGoogleGenerativeAI:
    """
    Get LLM instance by type. Returns cached instance if available.
    If use_local_model is True, it will attempt to use the local Qwen model.
    """
    if use_local_model:
        class LocalLLMWrapper:
            def invoke(self, prompt: str):
                return local_llm_client.generate_response(prompt, use_local_model=True)
            def stream(self, prompt: str):
                yield self.invoke(prompt)
            def bind_tools(self, tools):
                # This is a no-op for the local model as it doesn't support tool calling directly
                return self

        return LocalLLMWrapper()

    if llm_type in _llm_cache:
        return _llm_cache[llm_type]

    if llm_type == "reasoning":
        # Automatic detection and fallback for Chinese APIs
        if "qwq-plus" in REASONING_MODEL.lower() or "aliyuncs" in REASONING_MODEL.lower():
            print("Detected Chinese API for reasoning model. Falling back to Gemini.")
            model_to_use = "gemini-2.0-flash"
            api_key_to_use = REASONING_API_KEY # Assuming REASONING_API_KEY is now GEMINI_API_KEY
        else:
            model_to_use = REASONING_MODEL
            api_key_to_use = REASONING_API_KEY

        llm = create_gemini_llm(
            model=model_to_use,
            api_key=api_key_to_use,
        )
    elif llm_type == "basic":
        llm = create_gemini_llm(
            model=BASIC_MODEL,
            api_key=BASIC_API_KEY,
        )
    elif llm_type == "vision":
        llm = create_gemini_llm(
            model=VL_MODEL,
            api_key=VL_API_KEY,
        )
    else:
        raise ValueError(f"Unknown LLM type: {llm_type}")

    _llm_cache[llm_type] = llm
    return llm


# Initialize LLMs for different purposes - now these will be cached
reasoning_llm = get_llm_by_type("reasoning")
basic_llm = get_llm_by_type("basic")
vl_llm = get_llm_by_type("vision")


if __name__ == "__main__":
    # Test Gemini
    stream = reasoning_llm.stream("what is mcp?")
    full_response = ""
    for chunk in stream:
        full_response += chunk.content
    print(f"Gemini response: {full_response}")

    basic_llm.invoke("Hello")
    vl_llm.invoke("Hello")

    # Test local model
    local_reasoning_llm = get_llm_by_type("reasoning", use_local_model=True)
    local_response = local_reasoning_llm.invoke("what is mcp?")
    print(f"Local model response: {local_response}")


