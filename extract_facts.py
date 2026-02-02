# extract_facts.py

import json
from prompt_builder import build_prompt
from llama_client import call_llama
from json_validator import parse_llm_json

TARGET_SECTIONS = {"Methodology", "Related Work"}

def load_sections(path="sections.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    sections = load_sections()
    all_results = []

    for sec in sections:
        if sec["name"] not in TARGET_SECTIONS:
            continue

        print(f"🔍 Extracting from section: {sec['name']}")

        prompt = build_prompt(sec["text"])

        raw_output = call_llama(prompt)

        try:
            extracted = parse_llm_json(raw_output)
        except ValueError:
            print("❌ Invalid JSON, skipping section")
            continue

        result = {
            "paper_id": "paper_001",
            "section": sec["name"],
            "extracted_facts": extracted
        }

        all_results.append(result)

    with open("extracted_facts.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print("✅ Extraction complete → extracted_facts.json")

if __name__ == "__main__":
    main()
