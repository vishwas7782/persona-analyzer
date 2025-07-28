# Use AMD64-compatible slim Python base image
FROM --platform=linux/amd64 python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install system + Python dependencies + spaCy model + link it
RUN apt-get update && \
    apt-get install -y gcc libglib2.0-0 libgl1 libxrender1 libsm6 libxext6 && \
    pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download en_core_web_sm && \
    python -m spacy link en_core_web_sm en_core_web_sm && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy your application files
COPY . .

# Ensure input/output dirs exist
RUN mkdir -p /app/input /app/output

# Set entrypoint
ENTRYPOINT ["python", "main.py"]
