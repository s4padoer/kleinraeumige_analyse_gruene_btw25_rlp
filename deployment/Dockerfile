FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgeos-dev \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Kopiere nur die notwendigen Dateien für die Abhängigkeiten
COPY pyproject.toml uv.lock ./

RUN pip install uv && \
    uv pip compile pyproject.toml -o requirements.txt && \
    pip install -r requirements.txt && \
    pip uninstall -y uv && \
    rm requirements.txt

# Kopiere den Rest der Anwendung
COPY app .

# Installiere das Paket im "editable mode" (falls nötig)
RUN pip install -e .


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]