"""
AI Feedback Agent
-----------------
A small Flask API to analyze user feedback and generate short summaries
with actionable improvement suggestions.

This is a demo version using the Hugging Face google/flan-t5-small model.
Even if the AI call fails, the API always returns a JSON response for safe deployment.
"""

from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env (optional)
load_dotenv()

app = Flask(__name__)

# -------------------- CONFIG --------------------
# Model to use for summarizing feedback
HF_MODEL = os.getenv("HF_MODEL", "google/flan-t5-small")
HF_URL = "https://router.huggingface.co/hf-inference"  # Hugging Face router endpoint
HF_TOKEN = os.getenv("HF_TOKEN", "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")  # add your token to .env if available

HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

# -------------------- HELPERS --------------------
def query_hf(prompt: str, max_tokens: int = 150) -> str:
    """
    Sends a request to the Hugging Face router API.
    Returns the model's response, or a placeholder if the API fails.
    """
    payload = {
        "model": HF_MODEL,
        "inputs": prompt,
        "parameters": {"max_new_tokens": max_tokens},
    }

    try:
        response = requests.post(HF_URL, headers=HEADERS, json=payload, timeout=30)
    except requests.exceptions.RequestException as e:
        # API request failed, return placeholder
        return f"Demo placeholder: API call failed ({e})"

    if response.status_code == 200:
        try:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                return data[0].get("generated_text", "").strip()
            if isinstance(data, dict) and "error" in data:
                return f"Demo placeholder: API returned error ({data.get('error')})"
            return str(data)
        except ValueError:
            return "Demo placeholder: Invalid JSON from HF API"
    else:
        # Graceful fallback if API returns 404 or any other status
        return "Demo placeholder: model call failed. Summary + suggestions can be added here."

# -------------------- PROMPT TEMPLATE --------------------
PROMPT_TEMPLATE = (
    "You are a product analyst.\n"
    "Read the user feedback and return a short summary (1-2 lines) "
    "followed by 3 clear improvement suggestions.\n\n"
    "Feedback: {feedback}\n\nSummary and Suggestions:\n"
)

# -------------------- ROUTES --------------------
@app.route("/", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "AI Feedback Agent running (demo-ready)"})

@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Accepts JSON with 'feedback' field and returns a summary + suggestions.
    Uses the Hugging Face model or a placeholder if API fails.
    """
    data = request.get_json(force=True, silent=True)

    if not data or "feedback" not in data:
        return jsonify({"error": "POST JSON with 'feedback' field required"}), 400

    feedback = data["feedback"].strip()
    if not feedback:
        return jsonify({"error": "feedback cannot be empty"}), 400

    prompt = PROMPT_TEMPLATE.format(feedback=feedback)
    result = query_hf(prompt, max_tokens=200)

    return jsonify({"analysis": result})

# -------------------- RUN --------------------
if __name__ == "__main__":
    # Run locally on port 5000, enable debug mode for development
    app.run(host="0.0.0.0", port=5000, debug=True)
