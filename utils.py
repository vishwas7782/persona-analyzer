import re
import spacy
from collections import defaultdict

nlp = spacy.load("en_core_web_sm")  # Load spaCy model

def extract_text_by_page(doc):
    return [page.get_text() for page in doc]

def extract_keywords(text, top_n=20):
    doc = nlp(text)
    keywords = set()

    # Extract named entities (like locations, orgs)
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC", "ORG", "EVENT"]:
            keywords.add(ent.text.lower())

    # Extract noun chunks (like "wine tasting", "local food")
    for chunk in doc.noun_chunks:
        if len(chunk.text.split()) <= 3:
            keywords.add(chunk.text.lower())

    return list(keywords)[:top_n]

def match_sections(text, persona, job):
    matched_sections = []
    matched_subsections = []

    auto_keywords = extract_keywords(text)
    # print("Auto-extracted Keywords:", auto_keywords)

    for kw in auto_keywords:
        if re.search(rf"\b{re.escape(kw)}\b", text, re.IGNORECASE):
            lines = text.splitlines()
            for line in lines:
                if kw.lower() in line.lower():
                    if line.isupper() or line.istitle():
                        matched_sections.append(line.strip())
                    else:
                        matched_subsections.append(line.strip())

    return list(set(matched_sections)), list(set(matched_subsections))