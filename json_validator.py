# json_validator.py

import json

def parse_llm_json(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        raise ValueError("LLM output is not valid JSON")
