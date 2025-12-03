import os
from flask import Flask, render_template, request
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
API_TOKEN = os.getenv("HF_API_TOKEN")
if not API_TOKEN:
    raise ValueError("HF_API_TOKEN not found in environment variables")

client = InferenceClient(token=API_TOKEN)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/summer", methods=["POST"])
def summer():
    try:
        data = request.form.get("data")
        max_length = int(request.form.get("maxl", 100))
        min_length = 20

        if not data:
            return render_template("index.html", result="Please enter some text.")

        # Using the summarization task directly
        summary_output = client.summarization(
            data,
            model="facebook/bart-large-cnn"
        )
        
        # The output is typically a SummarizationOutput object or a list/dict depending on version
        # Based on my test, it returns an object with summary_text attribute
        if hasattr(summary_output, 'summary_text'):
             return render_template("index.html", result=summary_output.summary_text)
        elif isinstance(summary_output, list) and len(summary_output) > 0 and 'summary_text' in summary_output[0]:
             return render_template("index.html", result=summary_output[0]['summary_text'])
        else:
             # Fallback for string or other formats
             return render_template("index.html", result=str(summary_output))

    except Exception as e:
        return render_template("index.html", result=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
