FROM python:3.12-slim

# Installiere Systemabhängigkeiten
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    make \
    && rm -rf /var/lib/apt/lists/*

# Kopiere die Abhängigkeitsdateien und installiere sie
COPY pyproject.toml uv.lock ./
RUN pip install uv

# Kopiere den Rest der Anwendung
COPY app .

# Installiere das Paket (nicht im editable mode)
RUN uv pip sync uv.lock --system --no-cache-dir

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]