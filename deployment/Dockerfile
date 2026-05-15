FROM python:3.12-slim

WORKDIR /app

# Installiere uv
RUN pip install uv

# Kopiere die uv.lock-Datei und installiere die Abhängigkeiten
COPY uv.lock .
RUN uv pip sync uv.lock

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]