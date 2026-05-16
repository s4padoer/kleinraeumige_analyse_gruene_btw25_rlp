FROM python:3.12-slim

# Installiere Systemabhängigkeiten
RUN apt-get update 

# Kopiere die Abhängigkeitsdateien und installiere sie
COPY pyproject.toml uv.lock ./
RUN pip install uv && \
    uv pip compile pyproject.toml -o requirements.txt && \
    pip install -r requirements.txt && \
    pip uninstall -y uv && \
    rm requirements.txt

# Kopiere den Rest der Anwendung
COPY app .

# Installiere das Paket (nicht im editable mode)
RUN pip install .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]