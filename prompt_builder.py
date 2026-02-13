import json
from schema import EXTRACTION_SCHEMA

def build_prompt(section_text: str) -> str:
    schema_str = json.dumps(EXTRACTION_SCHEMA, indent=2)

    prompt = f"""
You are an expert AI research assistant extracting data from a research paper.

Extract the following:
1. "datasets": A list of dataset names used for training/testing. 
   - CRITICAL: DO NOT include model architectures (like YOLO, ResNet, CNN, LSTM) in this list. 
   - If the paper uses a custom dataset without a name, extract a short description like "custom private dataset" or "simulated cloud data".
2. "experiment": A list of AI/ML models evaluated. Extract the model name and its numerical evaluation metrics (e.g., Accuracy, F1, RMSE, MOTA).

IMPORTANT INSTRUCTIONS:
- For "result", use the exact metric name as the key (e.g., "MOTA") and the numerical score as the value.
- If a metric is not found for a model, omit it.
- Return STRICTLY valid JSON matching the schema below.

Schema:
{schema_str}

Text to analyze:
<<<
{section_text}
>>>
"""
    return prompt.strip()