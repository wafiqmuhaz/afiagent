import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Reasoning LLM configuration (for complex reasoning tasks)
REASONING_MODEL = os.getenv("REASONING_MODEL", "gemini-2.0-flash")
REASONING_API_KEY = os.getenv("GEMINI_API_KEY")

# Non-reasoning LLM configuration (for straightforward tasks)
BASIC_MODEL = os.getenv("BASIC_MODEL", "gemini-2.0-flash")
BASIC_API_KEY = os.getenv("GEMINI_API_KEY")

# Vision-language LLM configuration (for tasks requiring visual understanding)
VL_MODEL = os.getenv("VL_MODEL", "gemini-2.0-flash")
VL_API_KEY = os.getenv("GEMINI_API_KEY")

# Chrome Instance configuration
CHROME_INSTANCE_PATH = os.getenv("CHROME_INSTANCE_PATH")

# Tavily API Key
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


