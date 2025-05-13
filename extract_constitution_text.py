import os
import json
import re
from PyPDF2 import PdfReader

# Define paths
INPUT_PDF_PATH = 'data/raw/constitution/constitution.pdf'
OUTPUT_JSON_PATH = 'data/processed/cleaned_constitution.json'

def extract_constitution_to_json():
    if not os.path.exists(INPUT_PDF_PATH):
        print(f"[ERROR] PDF not found at: {INPUT_PDF_PATH}")
        return

    print("[INFO] Processing Constitution PDF (chapter-based)...")
    reader = PdfReader(INPUT_PDF_PATH)

    # Collect all pages with text
    pages = []
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if text:
            pages.append({
                "page": i,
                "text": text.strip()
            })
        else:
            print(f"[WARNING] Page {i} has no extractable text.")

    print(f"[INFO] Total pages processed: {len(pages)}")

    # Adjusted regex for identifying chapter headings
    chapter_regex = re.compile(r'^(CHAPTER\s+[IVXLC0-9]+\s*[:\-]?\s*.*)$', re.IGNORECASE)

    chapters = []
    current_chapter = None

    for page in pages:
        lines = page['text'].split('\n')
        for line in lines:
            line = line.strip()
            match = chapter_regex.match(line)
            if match:
                if current_chapter:
                    chapters.append(current_chapter)
                current_chapter = {
                    "chapter_title": match.group(1),
                    "text": "",
                    "start_page": page['page']
                }
            elif current_chapter:
                current_chapter["text"] += line + " "

    if current_chapter:
        chapters.append(current_chapter)

    print(f"[INFO] Total chapters extracted: {len(chapters)}")

    # ---- Rewriting code part ----
    # Only overwrite the file if content has changed
    existing_data = None
    if os.path.exists(OUTPUT_JSON_PATH):
        with open(OUTPUT_JSON_PATH, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                print("[WARNING] Existing JSON file is not valid. It will be overwritten.")

    if existing_data != chapters:
        os.makedirs(os.path.dirname(OUTPUT_JSON_PATH), exist_ok=True)
        with open(OUTPUT_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(chapters, f, ensure_ascii=False, indent=2)
        print(f"[SUCCESS] Extracted and saved {len(chapters)} chapters to: {OUTPUT_JSON_PATH}")
    else:
        print("[INFO] No changes detected. Output file not overwritten.")

if __name__ == "__main__":
    extract_constitution_to_json()
