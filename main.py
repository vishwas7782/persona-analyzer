import os
import json
import fitz  # PyMuPDF
import datetime
import logging
from typing import List, Tuple

from utils import extract_text_by_page, match_sections

INPUT_DIR = "input"
OUTPUT_DIR = "output"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_persona_job() -> Tuple[str, str]:
    try:
        with open(os.path.join(INPUT_DIR, "persona.txt"), "r", encoding="utf-8") as f:
            lines = f.readlines()
        persona = lines[0].strip().replace("Persona: ", "")
        job = lines[1].strip().replace("Job: ", "")
        logging.info(f"Loaded persona: {persona}, job: {job}")
        return persona, job
    except Exception as e:
        logging.error("Failed to load persona.txt")
        raise e

def rank_items_by_length(items: List[dict], key: str, top_n: int) -> List[dict]:
    sorted_items = sorted(items, key=lambda x: len(x[key]), reverse=True)
    for i, item in enumerate(sorted_items[:top_n]):
        item["importance_rank"] = i + 1
    return sorted_items[:top_n]

def process_documents():
    persona, job = load_persona_job()

    output = {
        "metadata": {
            "documents": [],
            "persona": persona,
            "job": job,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        },
        "sections": [],
        "subsections": []
    }

    doc_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".pdf")]
    if not doc_files:
        logging.warning("No PDF files found in input directory.")
        return

    output["metadata"]["documents"] = doc_files
    section_results, subsection_results = [], []

    for doc_file in doc_files:
        file_path = os.path.join(INPUT_DIR, doc_file)
        try:
            pdf = fitz.open(file_path)
            for page_num in range(len(pdf)):
                page_text = pdf[page_num].get_text()
                sections, subsections = match_sections(page_text, persona, job)
                section_results.extend([{
                    "document": doc_file,
                    "page": page_num + 1,
                    "section_title": sec,
                    "importance_rank": 0
                } for sec in sections])
                subsection_results.extend([{
                    "document": doc_file,
                    "page": page_num + 1,
                    "refined_text": sub,
                    "importance_rank": 0
                } for sub in subsections])
        except Exception as e:
            logging.error(f"Failed to process {doc_file}: {e}")

    output["sections"] = rank_items_by_length(section_results, "section_title", 10)
    output["subsections"] = rank_items_by_length(subsection_results, "refined_text", 10)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, "output.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    logging.info(f"Output written to {output_path}")

if __name__ == "__main__":
    logging.info("Started processing documents")
    process_documents()