import os
import json
import hashlib
import re
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract



INPUT_DIR = 'data/raw/supreme_court_cases/'
OUTPUT_FILE = 'data/processed/cleaned_cases.json'

def extract_text_from_pdf(path):
    try:
        reader = PdfReader(path)
        full_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text.strip() + "\n"
        return full_text if full_text.strip() else None
    except:
        return None

def extract_text_with_ocr(path):
    print(f"[INFO] Falling back to OCR for: {os.path.basename(path)}")
    try:
        images = convert_from_path(path)
        return "\n".join([pytesseract.image_to_string(img) for img in images]).strip()
    except Exception as e:
        print(f"[ERROR] OCR failed for {path}: {e}")
        return None

def summarize_case(text):
    if "ORDER" in text:
        start = text.index("ORDER")
        lines = text[start:].splitlines()[1:]
        non_empty = [line.strip() for line in lines if line.strip()]
        return " ".join(non_empty[:3])  # Short summary
    return ""

def extract_metadata(text, filename):
    title = ""
    petitioner = ""
    respondents = ""
    legal_focus = ""
    verdict = ""

    # Case title (from vs line)
    vs_match = re.search(r"(.+?)\s+versus\s+(.+?)\n", text, re.IGNORECASE)
    if vs_match:
        title = f"{vs_match.group(1).strip()} vs {vs_match.group(2).strip()}"
        petitioner = vs_match.group(1).strip()
        respondents = vs_match.group(2).strip()

    # Judges
    judges = list(set(re.findall(r"Justice\s+([A-Za-z\s]+)", text)))

    # Date
    date_match = re.search(r"Date of Hearing:\s*(\d{2}\.\d{2}\.\d{4})", text)
    date_of_hearing = date_match.group(1) if date_match else ""

    # Lawyers
    pet_lawyer = re.search(r"For the Petitioner.*?Mr\.\s+(.+?),?\s*ASC", text, re.IGNORECASE)
    resp_lawyer = re.search(r"For the Respondent.*?Mr\.\s+(.+?),?\s*ASC", text, re.IGNORECASE)

    # Legal reference (Act, Article or Section)
    law_match = re.search(r"section\s+(\d+[A-Za-z]*)\s+of\s+the\s+([A-Za-z\s]+Act,\s*\d{4})", text, re.IGNORECASE)
    if law_match:
        legal_focus = f"Section {law_match.group(1)} of the {law_match.group(2)}"

    # Verdict (short)
    verdict_match = re.search(r"(petition is|appeal is|dismissed|allowed)[^.]{0,100}\.", text, re.IGNORECASE)
    if verdict_match:
        verdict = verdict_match.group(0).strip()

    return {
        "filename": filename,
        "title": title,
        "justices": judges,
        "date_of_hearing": date_of_hearing,
        "petitioner": petitioner,
        "respondents": respondents,
        "lawyers": {
            "for_petitioner": pet_lawyer.group(1).strip() if pet_lawyer else "",
            "for_respondent": resp_lawyer.group(1).strip() if resp_lawyer else ""
        },
        "summary": summarize_case(text),
        "legal_focus": legal_focus,
        "verdict": verdict
    }

def compute_hash(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def extract_supreme_cases_to_json():
    if not os.path.exists(INPUT_DIR):
        print(f"[ERROR] Directory not found: {INPUT_DIR}")
        return

    print("[INFO] Extracting Supreme Court cases...")
    cleaned_cases = []
    files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith('.pdf')])

    if not files:
        print("[WARNING] No PDF files found.")
        return

    for filename in files:
        path = os.path.join(INPUT_DIR, filename)
        text = extract_text_from_pdf(path) or extract_text_with_ocr(path)

        if not text:
            print(f"[WARNING] No text extracted from {filename}. Skipping.")
            continue

        case_data = extract_metadata(text, filename)
        cleaned_cases.append(case_data)

    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            old_data = json.load(f)
        if compute_hash(old_data) == compute_hash(cleaned_cases):
            print("[INFO] No changes detected. Skipping JSON rewrite.")
            print(f"[INFO] Total cases processed: {len(cleaned_cases)} (unchanged)")
            return

    # === REWRITING CODE PART ===
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(cleaned_cases, f, ensure_ascii=False, indent=2)

    print(f"[SUCCESS] Extracted and saved {len(cleaned_cases)} cases into {OUTPUT_FILE}")

if __name__ == "__main__":
    extract_supreme_cases_to_json()
