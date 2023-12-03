import requests
import json

from src.templates import get_system_prompt

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
