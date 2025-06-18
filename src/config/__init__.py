from .env import (
    # Reasoning LLM
    REASONING_MODEL,
    REASONING_API_KEY,
    # Basic LLM
    BASIC_MODEL,
    BASIC_API_KEY,
    # Vision-language LLM
    VL_MODEL,
    VL_API_KEY,
    # Other configurations
    CHROME_INSTANCE_PATH,
    TAVILY_API_KEY,
)
from .tools import TAVILY_MAX_RESULTS

# Team configuration
TEAM_MEMBERS = ["researcher", "coder", "browser", "reporter"]

__all__ = [
    # Reasoning LLM
    "REASONING_MODEL",
    "REASONING_API_KEY",
    # Basic LLM
    "BASIC_MODEL",
    "BASIC_API_KEY",
    # Vision-language LLM
    "VL_MODEL",
    "VL_API_KEY",
    # Other configurations
    "TEAM_MEMBERS",
    "TAVILY_MAX_RESULTS",
    "CHROME_INSTANCE_PATH",
    "TAVILY_API_KEY",
]


