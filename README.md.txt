# AI Feedback Agent

Small Flask API that turns user feedback into a short summary + 3 improvement suggestions using a free Hugging Face model.

## Quick start
1. Create virtual env and install:
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirements.txt
2. Run:
python main.py
3. Test:
curl -X POST http://127.0.0.1:5000/analyze