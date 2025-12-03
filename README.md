https://rishi2000goku.pythonanywhere.com/

# TextSummarizer

\*\*web app using flask and distilbart that help user to Summarize there text
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

---

# Project Name

Briefly describe your app here, mentioning its main functionality and purpose.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Setting up the Environment](#setting-up-the-environment)
- [Running the App](#running-the-app)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Contributing](#contributing)

---

## Prerequisites

Make sure the following are installed on your system before proceeding:

- **Python** (version 3.7 or higher)
- **Pip** (Python package installer)
- **Git** (for cloning the repository)

You can check the installations by running:

bash
python --version
pip --version
git --version

git clone https://github.com/your-username/TextSummarizer.git
cd TextSummarizer

2. Set up a Virtual Environment (Recommended)
   Create a virtual environment to manage your dependencies locally:

bash
Copy code
python -m venv venv
Activate the virtual environment:

Windows:
bash
Copy code
venv\Scripts\activate
macOS/Linux:
bash
Copy code
source venv/bin/activate 3. Install Dependencies
All required packages are listed in requirements.txt. To install them, run:

bash
Copy code
pip install -r requirements.txt
Setting up the Environment
If your app uses environment variables (such as API keys or database credentials), create a .env file in the root directory of your project and define the variables like so:

plaintext
Copy code
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
Ensure you have the python-dotenv package to load environment variables automatically.

bash
Copy code
pip install python-dotenv
Running the App
To start the app, follow these steps:

Activate the virtual environment (if it’s not already activated).

Run the main application file. Replace main.py with the entry point of your app:

bash
Copy code
python main.py
Access the app:

For web applications, open your browser and navigate to http://127.0.0.1:5000 (or the specified port).
For command-line applications, follow any additional instructions specific to the CLI.
Dependencies
All dependencies are listed in requirements.txt. To update or add new dependencies, install the package using pip install and then run:

bash
Copy code
pip freeze > requirements.txt
This updates the requirements.txt file to include all packages currently installed in your environment.

---

Additional Tips

1. README.md Placement\*\*: This file should be placed in the root directory of your GitHub repository, as GitHub will automatically display it on the main page.
2. Updating Requirements\*\*: Whenever you add a new package, remember to update `requirements.txt` using `pip freeze > requirements.txt`.
3. **.gitignore**: Add `.env`, `venv/`, and other sensitive or local files to your `.gitignore` to keep them out of version control.

This setup will guide users through the installation and execution of your app and make it easy for others to contribute. Let me know if you want more specific content for any section!

## Challenges Faced & Solutions

During the development and debugging of this project, several challenges were encountered and resolved:

1.  **API Deprecation**:

    - **Issue**: The original Hugging Face API URL (`https://api-inference.huggingface.co/...`) was deprecated and returned 404/503 errors.
    - **Solution**: Switched to the official `huggingface_hub` Python library, which automatically handles the correct API endpoints and connection details.

2.  **JSON Parsing Errors**:

    - **Issue**: The application crashed with `Expecting value: line 1 column 1` because the deprecated API URL was returning HTML error pages instead of JSON.
    - **Solution**: Debugged by inspecting the raw response text. The switch to `huggingface_hub` resolved the underlying cause.

3.  **Security Vulnerabilities**:

    - **Issue**: The Hugging Face API token was hardcoded in `app.py`, causing GitHub push protection to block the commit.
    - **Solution**: Moved the API token to a `.env` file (added to `.gitignore`) and updated the application to load it using `python-dotenv`.

4.  **Code Complexity**:
    - **Issue**: The initial `app.py` had complex class structures, retry logic (`tenacity`), and caching (`lru_cache`) that made debugging difficult.
    - **Solution**: Refactored the application into a simple, functional Flask app, removing unnecessary dependencies (`tenacity`, `numpy`, `pandas`) to improve maintainability.

## Contributing

Fork the repository.
Create a new branch for your feature (git checkout -b feature-name).
Make your changes and commit (git commit -am 'Add new feature').
Push to the branch (git push origin feature-name).
Create a new Pull Request.
