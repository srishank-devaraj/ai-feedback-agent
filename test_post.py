import requests

def test_analyze():
    url = "http://127.0.0.1:5000/analyze"
    payload = {"feedback":"The dashboard loads slowly on mobile and charts don't render sometimes."}
    r = requests.post(url, json=payload, timeout=30)
    assert r.status_code == 200
    data = r.json()
    assert "analysis" in data and len(data["analysis"]) > 0
