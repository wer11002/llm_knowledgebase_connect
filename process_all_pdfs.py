import os
import fitz
import json

from prompt_builder import build_prompt
from llama_client import call_llama
from json_validator import parse_llm_json

# =========================
# CONFIGURATION
# =========================
# Changed from "pdf" to "pdfs" to match your terminal output
PDF_FOLDER = "pdfs" 

# =========================
# 1. FULL TEXT EXTRACTION
# =========================
def extract_full_text_from_pdf(pdf_path):
    """Reads the entire PDF and returns it as a single string."""
    try:
        doc = fitz.open(pdf_path)
        full_text = ""
        for page_index in range(len(doc)):
            # Get text and clean up basic spacing
            page_text = doc[page_index].get_text("text").strip()
            full_text += page_text + "\n\n"
        doc.close()
        return full_text.strip()
    except Exception as e:
        print(f"  ⚠️ Could not read PDF {pdf_path}. Error: {e}")
        return None

# =========================
# 2. MAIN BATCH PIPELINE
# =========================
def main():
    if not os.path.exists(PDF_FOLDER):
        print(f"❌ Folder '{PDF_FOLDER}' not found.")
        return

    all_results = {} # Starts as an empty dictionary to group by paper ID
    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith(".pdf")]
    
    if not pdf_files:
        print(f"⚠️ No PDF files found in '{PDF_FOLDER}'.")
        return

    print(f"🚀 Found {len(pdf_files)} PDFs to process.")

    for filename in pdf_files:
        pdf_path = os.path.join(PDF_FOLDER, filename)
        paper_id = os.path.splitext(filename)[0] # e.g., "paper1"
        
        # Initialize the paper structure
        if paper_id not in all_results:
            all_results[paper_id] = {"datasets": [], "experiment": []}
            
        print(f"\n📄 Processing: {filename}")
        
        # 1. Get ALL text from the PDF
        full_text = extract_full_text_from_pdf(pdf_path)
        
        if not full_text: 
            continue 
            
        print(f"  🔍 Extracting facts from the entire document...")
        
        # 2. Send the full text to the LLM
        prompt = build_prompt(full_text)
        raw_output = call_llama(prompt)

        # 3. Parse and merge the results
        try:
            extracted = parse_llm_json(raw_output)
            
            if isinstance(extracted, dict):
                new_datasets = extracted.get("datasets", [])
                new_experiments = extracted.get("experiment", [])
                
                if isinstance(new_datasets, list):
                    all_results[paper_id]["datasets"].extend(new_datasets)
                if isinstance(new_experiments, list):
                    all_results[paper_id]["experiment"].extend(new_experiments)
                
                # Remove duplicate datasets (convert list to set and back to list)
                all_results[paper_id]["datasets"] = list(set(all_results[paper_id]["datasets"]))

        except ValueError:
            print("  ❌ Invalid JSON returned by LLM for this paper.")
            continue

    # Save final output
    output_file = "all_extracted_facts.json"
    if all_results:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Batch extraction complete! All results saved to {output_file}")
    else:
        print("\n⚠️ Finished, but no data was extracted.")

if __name__ == "__main__":
    main()