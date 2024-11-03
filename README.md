# TextSummarizer

**web app using flask and distilbart that help user to Summarize there text
This code defines a web application for text summarization using Flask and a frontend with a user-friendly, modern design. It utilizes the Hugging Face BART model to perform AI-powered summarization. Here’s an overview of the functionality:

Backend (Python with Flask)
Flask Setup: Initializes the Flask application with routing and error handling.
Summarizer Configuration: Contains settings for the API, rate limiting, and cache size to manage API calls and retries efficiently.
Text Summarizer Class:
Rate Limiting: Implements rate limiting to avoid overwhelming the API.
API Request Handling: Includes retry logic to handle transient failures and delays if the model is loading.
Summarization: Utilizes caching to store responses and reduce repeated API calls for identical requests.
Endpoints:
index(): Serves the main page.
summer(): Handles text summarization requests, validates inputs, and returns the summarized text or error messages.
Frontend (HTML and JavaScript)
HTML Structure: Built with Bootstrap for a responsive design and FontAwesome for icons.
Features Section: Highlights the summarizer's capabilities (e.g., quick summary, AI-powered, adjustable length).
Form Input: Text area for input with a character counter and adjustable slider for summary length.
Dark Mode Toggle: Allows users to switch to dark mode for a more comfortable viewing experience.
Loading Animation: Provides feedback while the API processes the request.
Summary Result Display: Shows the summarized text with a copy-to-clipboard button for convenience.
This setup offers a user-friendly experience by blending a clean UI with the power of API-driven summarization, handling errors and model loading states efficiently.
*******
