import logging
import requests
from .qwen_client import QwenClient

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self, model_path: str = "assets/model/DeepSeek-R1-Distill-Qwen-1.5B-Q5_K_M.gguf"):
        self.qwen_client = QwenClient(model_path=model_path)

    def crawl(self, url: str, return_format: str = "html", use_local_model: bool = False) -> str:
        if use_local_model:
            # For tasks like HTML parsing, info retrieval, data extraction
            prompt = f"Extract the main content from the following URL: {url}"
            return self.qwen_client.generate_response(prompt)
        else:
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for HTTP errors
                return response.text
            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching URL {url}: {e}")
                return ""

    def generate_response(self, prompt: str, use_local_model: bool = False) -> str:
        if use_local_model:
            # For direct answers, modify the prompt to encourage a concise response
            modified_prompt = f"Provide a concise answer to the following question: {prompt}"
            return self.qwen_client.generate_response(modified_prompt)
        else:
            # Placeholder for Gemini API call - integrate actual Gemini API here
            # For now, just return a dummy response or raise an error if Gemini is not set up
            logger.warning("Gemini API not implemented. Using dummy response.")
            return f"[Gemini API response for: {prompt}]"

