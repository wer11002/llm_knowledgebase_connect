import json
import re

# =========================
# SECTION HEADER PATTERNS
# =========================
SECTION_PATTERNS = {
    "Abstract": r"^\s*(abstract)\s*$",
    "Introduction": r"^\s*(\d+\.|I\.)?\s*(introduction)\s*$",
    "Related Work": r"^\s*(\d+\.|II\.)?\s*(related work|literature review|background)\s*$",
    "Methodology": r"^\s*(\d+\.|III\.)?\s*(methodology|method|approach|proposed method|system architecture)\s*$",
    "Experiments": r"^\s*(\d+\.|IV\.)?\s*(experiments?|experimental results|experimental evaluation|results|evaluation|performance analysis)\s*$",
    "Conclusion": r"^\s*(\d+\.|V\.)?\s*(conclusion|conclusions|discussion|future work)\s*$",
    "Acknowledgment": r"^\s*(acknowledg(e)?ment(s)?)\s*$",
    "References": r"^\s*(references|bibliography)\s*$"
}

MAX_SECTION_PAGES = 6   # allow realistic spread

# =========================
# CLEAN PAGE TEXT
# =========================
def clean_page_text(text):
    lines = text.split("\n")
    cleaned = []

    for line in lines:
        s = line.strip().lower()

        if s.isdigit():
            continue
        if "ieee access" in s:
            continue
        if "volume" in s and "number" in s:
            continue
        if "received" in s and "accepted" in s:
            continue

        cleaned.append(line)

    return cleaned

# =========================
# HEADER DETECTION
# =========================
def is_section_header(line):
    clean = line.strip()

    if len(clean) > 60:
        return None
    if len(clean.split()) > 6:
        return None

    for name, pattern in SECTION_PATTERNS.items():
        if re.match(pattern, clean, re.IGNORECASE):
            return name

    return None

# =========================
# SECTION EXTRACTION
# =========================
def detect_sections(pages):
    sections = []

    current_section = None
    current_pages = set()
    current_lines = []

    for page in pages:
        page_num = page.get("page_number", 0)
        lines = clean_page_text(page.get("text", ""))

        for line in lines:
            header = is_section_header(line)

            # ---------------------
            # NEW SECTION FOUND
            # ---------------------
            if header:
                # save previous section
                if current_section:
                    sections.append({
                        "name": current_section,
                        "pages": sorted(current_pages),
                        "text": "\n".join(current_lines).strip()
                    })

                # skip storing Acknowledgment (boundary only)
                if header == "Acknowledgment":
                    current_section = None
                    current_pages = set()
                    current_lines = []
                    continue

                # start new section
                current_section = header
                current_pages = {page_num}
                current_lines = []
                continue

            # ---------------------
            # COLLECT CONTENT
            # ---------------------
            if current_section:
                if len(current_pages) <= MAX_SECTION_PAGES:
                    current_pages.add(page_num)
                    current_lines.append(line)

    # save last section
    if current_section:
        sections.append({
            "name": current_section,
            "pages": sorted(current_pages),
            "text": "\n".join(current_lines).strip()
        })

    return sections

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    try:
        with open("pages.json", "r", encoding="utf-8") as f:
            pages = json.load(f)

        sections = detect_sections(pages)

        with open("sections.json", "w", encoding="utf-8") as f:
            json.dump(sections, f, indent=2, ensure_ascii=False)

        print("✅ Success! Check sections.json\n")

        for sec in sections:
            print(f"📂 {sec['name']} - {len(sec['pages'])} pages - {len(sec['text'])} chars")

    except FileNotFoundError:
        print("❌ Error: pages.json not found")
