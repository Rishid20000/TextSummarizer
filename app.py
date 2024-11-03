# please make hugging face token(api key) (https://huggingface.co/settings/tokens) to run this app and install all dependency of python 
#singup on hugging face and go to https://huggingface.co/settings/tokens this link after signup 
#after generating token paste at line 20 in  place of your api key  (API_TOKEN = "your hugging face api keys" )

from flask import Flask, render_template, request, jsonify
import requests
from typing import Dict, Any, Optional
import logging
import time
from functools import lru_cache
from tenacity import retry, stop_after_attempt, wait_exponential

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SummarizerConfig:
    """Configuration class for the summarizer application."""
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    API_TOKEN = "your hugging face api keys" 
    MIN_LENGTH = 20
    MAX_LENGTH = 200
    CACHE_SIZE = 100
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds
    REQUEST_TIMEOUT = 30  # seconds

class TextSummarizer:
    """Handles text summarization using the Hugging Face API."""
    
    def __init__(self, config: SummarizerConfig):
        self.config = config
        self.headers = {"Authorization": f"Bearer {config.API_TOKEN}"}
        self.last_request_time = 0
        self.rate_limit_delay = 1  # seconds between requests
        
    def _check_rate_limit(self):
        """Implement basic rate limiting."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last_request)
        self.last_request_time = time.time()

    def _handle_model_loading(self, response: requests.Response) -> bool:
        """Handle the case where the model is still loading."""
        try:
            response_json = response.json()
            if isinstance(response_json, dict) and response_json.get("error") == "Model facebook/bart-large-cnn is currently loading":
                logger.info("Model is loading, waiting before retry...")
                time.sleep(self.config.RETRY_DELAY)
                return True
            return False
        except Exception:
            return False

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _make_api_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Make API request with retry logic."""
        self._check_rate_limit()
        
        response = requests.post(
            self.config.API_URL,
            headers=self.headers,
            json=payload,
            timeout=self.config.REQUEST_TIMEOUT
        )
        
        # Handle model loading state
        if response.status_code == 503 or self._handle_model_loading(response):
            raise requests.exceptions.RequestException("Model is loading")
            
        response.raise_for_status()
        return response.json()

    @lru_cache(maxsize=SummarizerConfig.CACHE_SIZE)
    def summarize(self, text: str, max_length: int) -> Dict[str, Any]:
        """
        Summarize the given text using the Hugging Face API.
        
        Args:
            text: Input text to summarize
            max_length: Maximum length of the summary
            
        Returns:
            Dictionary containing the summary or error message
        """
        try:
            payload = {
                "inputs": text,
                "parameters": {
                    "min_length": self.config.MIN_LENGTH,
                    "max_length": max_length
                }
            }
            
            output = self._make_api_request(payload)
            
            if isinstance(output, list) and output and "summary_text" in output[0]:
                return {"success": True, "summary": output[0]["summary_text"]}
            else:
                logger.error(f"Unexpected API response format: {output}")
                return {
                    "success": False, 
                    "error": "Invalid API response format. Please try again."
                }
                
        except requests.exceptions.Timeout:
            logger.error("API request timed out")
            return {
                "success": False, 
                "error": "Request timed out. The service might be experiencing high load. Please try again in a few moments."
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            return {
                "success": False, 
                "error": "The summarization service is temporarily unavailable. Please try again in a few moments."
            }
            
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {
                "success": False, 
                "error": "An unexpected error occurred. Please try again later."
            }

# Initialize Flask application
app = Flask(__name__)
summarizer = TextSummarizer(SummarizerConfig())

@app.route("/", methods=["GET"])
def index() -> str:
    """Render the main page."""
    return render_template("index.html")

@app.route("/summer", methods=["POST"])
def summer() -> str:
    """Handle summarization requests."""
    try:
        # Validate input
        text = request.form.get("data", "").strip()
        if not text:
            return render_template("index.html", 
                                result="Please provide text to summarize.")
        
        # Check text length
        if len(text) > 50000:  # Add reasonable limit
            return render_template("index.html",
                                result="Text is too long. Please limit to 50,000 characters.")
        
        # Validate and convert max_length
        try:
            max_length = int(request.form.get("maxl", SummarizerConfig.MAX_LENGTH))
            max_length = min(max(max_length, SummarizerConfig.MIN_LENGTH), 
                           SummarizerConfig.MAX_LENGTH)
        except ValueError:
            max_length = SummarizerConfig.MAX_LENGTH
        
        # Get summary
        result = summarizer.summarize(text, max_length)
        
        if result["success"]:
            return render_template("index.html", result=result["summary"])
        else:
            return render_template("index.html", result=result["error"])
            
    except Exception as e:
        logger.error(f"Error in summer route: {str(e)}")
        return render_template("index.html", 
                             result="An error occurred while processing your request.")

# Error handlers remain the same...

if __name__ == "__main__":
    app.run(debug=True)
