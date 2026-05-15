from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import geopandas as gpd
import json

import os
from pydantic import BaseModel
from pyrosm import get_data, OSM


app = FastAPI()
# Korrigierte Pfade: Relativ zum Skript (main.py)
static_dir = os.path.join(os.path.dirname(__file__), "static")
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
data_path = os.path.join(os.path.dirname(__file__), "data")

# Statische Dateien und Templates
app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

rlp_regions = gpd.read_file(os.path.join(data_path, "landkreise_with_predictions.geojson"))
# Liste der verfügbaren Regionen
print("Originales CRS:", rlp_regions.crs)  # Debugging

# Falls das CRS nicht EPSG:4326 ist, umwandeln
if rlp_regions.crs != "EPSG:4326":
    rlp_regions = rlp_regions.to_crs("EPSG:4326")
    print("Umgewandeltes CRS:", rlp_regions.crs)  
regions = rlp_regions["name"].unique().tolist() 

# Lade die vorbereiteten Daten
with open(os.path.join(data_path, "heatmap_data.json"), "r") as f:
    heatmap_data = json.load(f)

@app.get("/", response_class=HTMLResponse)
def read_root():
    # Lade den Inhalt der index.html und gib ihn als HTML-Response zurück
    with open(os.path.join(static_dir, "index.html"), "r", encoding="utf-8") as f:
        html_content = f.read()
    return Response(content=html_content, media_type="text/html")
    
@app.get("/landkreise")
def get_landkreise():
    """Gibt alle verfügbaren Landkreise zurück."""
    return {"landkreise": regions}

@app.get("/heatmap")
def get_heatmap():
    """Gibt alle Heatmap-Daten zurück (für alle Landkreise)."""
    return {"heatmap": heatmap_data}

@app.get("/bounds/{landkreis_name}")
def get_bounds(landkreis_name: str):
    """Gibt die Bounds (Grenzen) eines Landkreises zurück."""
    try:
        kreis_data = rlp_regions[rlp_regions["name"] == landkreis_name]
        if kreis_data.empty:
            raise HTTPException(status_code=404, detail="Landkreis nicht gefunden")

        # Berechne die Bounds des Landkreises
        bounds = kreis_data.total_bounds.tolist()  # [minx, miny, maxx, maxy]
        return {
            "bounds": [
                [bounds[1], bounds[0]],  # Südwest-Ecke (lat, lng)
                [bounds[3], bounds[2]]   # Nordost-Ecke (lat, lng)
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler: {e}")
    

@app.get("/straßen/{landkreis_name}")
def get_straßen(landkreis_name: str):
    """Lädt die Straßen für einen Landkreis dynamisch."""
    filename = landkreis_name.lower().replace(" ", "_")
    try:
        file_path = os.path.join(data_path, f"strassen_{filename}.gpkg")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Landkreis nicht gefunden")

        df = gpd.read_file(file_path)
        return json.loads(df.to_json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler: {e}")

@app.get("/heatmap")
def get_heatmap():
    return JSONResponse(content=heatmap_data)

@app.get("/bounds/{landkreis_name}")
def get_bounds(landkreis_name: str):
    try:
        kreis_data = rlp_regions[rlp_regions["name"] == landkreis_name]
        if kreis_data.empty:
            raise HTTPException(status_code=404, detail="Landkreis nicht gefunden")

        bounds = kreis_data.total_bounds.tolist()
        return JSONResponse(content={
            "bounds": [
                [bounds[1], bounds[0]],  # Südwest
                [bounds[3], bounds[2]]   # Nordost
            ]
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
