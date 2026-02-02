# prompt_builder.py

import json
from schema import EXTRACTION_SCHEMA

def build_prompt(section_text: str) -> str:
    schema_str = json.dumps(EXTRACTION_SCHEMA, indent=2)

    prompt = f"""
You are an information extraction system.

Extract the following information from the text:
- Dataset names
- Model names
- Evaluation metrics
- Numerical results (with metric and value)

Return STRICT JSON and nothing else.

Use this schema exactly:
{schema_str}

If an item is not mentioned, return an empty list.

Text:
<<<
{section_text}
>>>
"""
    return prompt.strip()
