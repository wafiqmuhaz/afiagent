# make / migrate to gemini
import logging
import requests

logger = logging.getLogger(__name__)


class GeminiClient:
    def crawl(self, url: str, return_format: str = "html") -> str:
        # For Gemini, we will directly fetch the URL content.
        # The return_format parameter is kept for compatibility but not directly used for content fetching.
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching URL {url}: {e}")
            return ""


