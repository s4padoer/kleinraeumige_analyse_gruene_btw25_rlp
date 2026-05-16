from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os
from shapely.geometry import shape

app = FastAPI()
# Korrigierte Pfade: Relativ zum Skript (main.py)
static_dir = os.path.join(os.path.dirname(__file__), "static")
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
data_path = os.path.join(os.path.dirname(__file__), "data")

# Statische Dateien und Templates
app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

# Lade die GeoJSON-Datei für Landkreise
with open(os.path.join(data_path, "landkreise_with_predictions.geojson"), "r", encoding="utf-8") as f:
    landkreise_data = json.load(f)

# Extrahiere die Namen der Landkreise
regions = [feature["properties"]["name"] for feature in landkreise_data["features"]]

@app.get("/", response_class=HTMLResponse)
def read_root():
    # Lade den Inhalt der index.html und gib ihn als HTML-Response zurück
    with open(os.path.join(static_dir, "index.html"), "r", encoding="utf-8") as f:
        html_content = f.read()
    return Response(content=html_content, media_type="text/html")

@app.get("/landkreise")
def get_landkreise():
    """Gibt alle verfügbaren Landkreise zurück."""
    return {"landkreise": set(regions)}

@app.get("/bounds/{landkreis_name}")
def get_bounds(landkreis_name: str):
    """Gibt die Bounds (Grenzen) eines Landkreises zurück."""
    try:
        # Suche den Landkreis in den Features
        feature = next(
            (f for f in landkreise_data["features"] if f["properties"]["name"] == landkreis_name),
            None
        )
        if not feature:
            raise HTTPException(status_code=404, detail="Landkreis nicht gefunden")

        # Berechne die Bounds des Landkreises
        geometry = shape(feature["geometry"])
        bounds = geometry.bounds  # (minx, miny, maxx, maxy)

        return JSONResponse(content={
            "bounds": [
                [bounds[1], bounds[0]],  # Südwest-Ecke (lat, lng)
                [bounds[3], bounds[2]]   # Nordost-Ecke (lat, lng)
            ]
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/strassen/{landkreis_name}")
def get_straßen(landkreis_name: str):
    """Lädt die Straßen für einen Landkreis mit 1km-Grid-Werten."""
    filename = landkreis_name.lower().replace(" ", "_")
    try:
        file_path = os.path.join(data_path, f"strassen_{filename}.geojson")

        if not os.path.exists(file_path):
            # Liste alle verfügbaren Dateien für Debugging
            print("Verfügbare Dateien:", os.listdir(data_path))
            raise HTTPException(status_code=404, detail=f"Datei nicht gefunden: {file_path}")

        # Lade die GeoJSON-Datei
        with open(file_path, "r", encoding="utf-8") as f:
            strassen_data = json.load(f)

        # Extrahiere die benötigten Daten (z. B. 'prediction2')
        # Hier kannst du die Daten direkt aus dem GeoJSON verwenden
        return JSONResponse(content=strassen_data)
    except Exception as e:
        print(f"Fehler: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Fehler: {str(e)}")