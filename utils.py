# utils.py
import httpx

def download_file(url: str) -> bytes:
    """Download any file (PDF/CSV/etc.) and return raw bytes."""
    print(f"[DOWNLOAD] Fetching: {url}")

    with httpx.Client(timeout=60.0) as client:
        resp = client.get(url)
        resp.raise_for_status()
        return resp.content


def submit_answer(url, email, secret, quiz_url, answer):
    payload = {
        "email": email,
        "secret": secret,
        "url": quiz_url,
        "answer": answer
    }

    print(f"[SUBMIT] Sending answer to {url}")

    with httpx.Client(timeout=60.0) as client:
        resp = client.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()