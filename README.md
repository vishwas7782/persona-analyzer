# Adobe India Hackathon 2025 - Challenge 2B

## Challenge: Persona-Driven Document Intelligence

### 🧠 Objective
Build a system that intelligently analyzes a collection of PDF documents and extracts the most relevant sections and sub-sections based on a given persona and job-to-be-done. The system should output a structured JSON with metadata, prioritized sections, and refined sub-sections.

---

## 🛠️ Approach

### 1. **Input Parsing**
- The system reads all `.pdf` files from the `/input` directory.
- It expects a `persona.txt` file in the same directory with the format:
```

Persona: <persona description>
Job: <job to be done>

````

### 2. **Text Extraction**
- Each PDF is processed page by page using `PyMuPDF` (fitz) to extract clean text.

### 3. **Keyword Extraction**
- The text is passed through a preloaded `spaCy` NLP model (`en_core_web_sm`) to extract:
- Named entities (ORG, LOC, GPE, EVENT)
- Noun chunks (phrases of interest, limited to 3 words)
- This yields a list of potential keywords representing what might be relevant in the context of the persona/job.

### 4. **Section & Sub-section Matching**
- Each extracted keyword is searched in the document lines.
- Lines that match and are title-like (ALL CAPS or Title Case) are treated as **sections**.
- Other lines with matches are treated as **sub-sections**.

### 5. **Ranking**
- Sections and sub-sections are sorted by length (as a proxy for information density).
- The top 10 most informative sections and sub-sections are selected.
- Each is assigned an `importance_rank`.

### 6. **Output JSON**
The final output JSON has the following structure:
```json
{
"metadata": {
  "documents": ["doc1.pdf", "doc2.pdf"],
  "persona": "PhD Researcher in Computational Biology",
  "job": "Prepare a literature review on drug discovery using GNNs",
  "timestamp": "2025-07-28T12:00:00Z"
},
"sections": [
  {
    "document": "doc1.pdf",
    "page": 2,
    "section_title": "INTRODUCTION TO GRAPH NEURAL NETWORKS",
    "importance_rank": 1
  },
  ...
],
"subsections": [
  {
    "document": "doc2.pdf",
    "page": 3,
    "refined_text": "The study explores how GNNs outperform traditional methods...",
    "importance_rank": 1
  },
  ...
]
}
````

---

## 📁 Directory Structure

```
persona-analyzer/
├── Dockerfile
├── requirements.txt
├── main.py
├── utils.py
├── input/             # (mounted volume with .pdfs and persona.txt)
├── output/            # (mounted volume where output.json is written)
```

---

## 🐳 Dockerization Details

### Build Image

```bash
docker build --platform linux/amd64 -t persona-analyzer .
```

### Run Container

```bash
docker build --platform linux/amd64 -t persona-analyzer .
docker run --rm -v ${PWD}\input:/app/input:ro -v ${PWD}\output:/app/output --network none persona-analyzer     
```

###  Dockerfile Highlights

* Base image: `python:3.10-slim`
* SpaCy model installed and linked:

  ```dockerfile
  RUN python -m spacy download en_core_web_sm && \
      python -m spacy link en_core_web_sm en_core_web_sm
  ```
* All dependencies installed in image (offline-compliant)

---

## 📦 Dependencies

```
PyMuPDF==1.23.21
spacy==3.7.2
```

---

## 📌 Constraints Handled

| Constraint               | Status     |
| ------------------------ | ---------- |
| CPU-only (amd64)         | ✅          |
| Model size < 1GB         | ✅ (\~50MB) |
| No Internet Access       | ✅          |
| Execution ≤ 60s (5 PDFs) | ✅          |
| JSON Output Format       | ✅          |

---

## 📌 Notes

* Code is modular and easily reusable in Round 2 webapp.
* Headings aren't solely determined by formatting — NLP context is used.
* Robust to varied document layouts.

---

## ✨ Future Improvements

* Add language detection and multilingual model fallback.
* Use semantic embedding + cosine similarity for more intelligent matching.
* Improve section relevance scoring using TF-IDF or fine-tuned classification.

---

## 👨‍💻 Authors

Team Hello World — Adobe India Hackathon 2025

```
**Vishwasjeet Kumar Gupta**  
BTech CSE | FullStack Developer  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/vishwasjeet-kumar-gupta-62814018a/)

**Tushar Kumar Chamlikar**  
BTech CSE | FullStack Developer  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/tushar-chamlikar-641726275/)
```
