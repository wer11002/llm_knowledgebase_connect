import fitz
import json

def extract_pdf_by_page(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []

    for page_index in range(len(doc)):
        page = doc[page_index]
        text = page.get_text("text")

        pages.append({
            "page_number": page_index + 1,
            "text": text.strip()
        })

    doc.close()
    return pages


pdf_path = "Stateless_System_Performance_Prediction_and_Health_Assessment_in_Cloud_Environments_Introducing_cSysGuard_an_Ensemble_Modeling_Approach.pdf"

pages = extract_pdf_by_page(pdf_path)

# ✅ SAVE RESULT
with open("pages.json", "w", encoding="utf-8") as f:
    json.dump(pages, f, indent=2, ensure_ascii=False)

print("Saved pages.json with", len(pages), "pages")
