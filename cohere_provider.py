import requests

def generate(prompt, system_prompt, model, api_key, timeout):
    url = "https://api.cohere.ai/v1/chat"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "message": prompt,
        "preamble": system_prompt
    }
    res = requests.post(url, headers=headers, json=payload, timeout=timeout)
    res.raise_for_status()
    return res.json()["text"]