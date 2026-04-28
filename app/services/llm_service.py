import requests
from app.config import Config


def generate_from_llm(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {Config.LLM_TOKEN}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(
        f"{Config.BASE_URL}/chat/completions",
        headers=headers,
        json=data,
    )

    if response.status_code != 200:
        print(f"LLM request failed with status {response.status_code}: {response.text}")
        raise Exception("LLM request failed")

    result = response.json()
    if "choices" in result and len(result["choices"]) > 0:
        return result["choices"][0]["message"]["content"]
    else:
        raise Exception("Invalid LLM response format")
