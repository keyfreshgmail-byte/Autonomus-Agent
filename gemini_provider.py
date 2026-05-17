import requests

def generate(prompt, system_prompt, model, api_key, timeout):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7}
    }
    headers = {"Content-Type": "application/json"}
    res = requests.post(url, headers=headers, json=payload, timeout=timeout)
    res.raise_for_status()
    return res.json()["candidates"][0]["content"]["parts"][0]["text"]