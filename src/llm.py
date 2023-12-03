import requests
import json

URL = "http://localhost:11434/api/generate"


def call_llm(model: str, system_prompt: str, prompt: str, first_name: str) -> str:
    response = requests.post(
        URL,
        data=json.dumps(
            {
                "model": model,
                "system": system_prompt,
                "prompt": prompt,
                "stream": False,
            }
        ),
    )

    return response.json()["response"]  
