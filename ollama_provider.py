import requests

def generate(prompt, system_prompt, model, base_url, timeout):
    url = f"{base_url.rstrip('/')}/api/chat"
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
        "stream": False
    }
    res = requests.post(url, json=payload, timeout=timeout)
    res.raise_for_status()
    return res.json()["message"]["content"]