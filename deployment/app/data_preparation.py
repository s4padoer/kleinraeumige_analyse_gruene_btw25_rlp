import os
import osmnx as ox
import geopandas as gpd

data_path = os.path.join(os.path.dirname(__file__), "data")

# GeoJSON-Daten laden
gdf = gpd.read_file(os.path.join(data_path, "zensus_1km_rlp_with_predictions.geojson"))


## Strassenzuege abspeichern, um das Laden zu reduzieren:
# Lade die Verwaltungsgrenzen von RLP
import os
import osmnx as ox
rlp_regions = gpd.read_file(os.path.join("deployment", "app", "data", "kreise-rlp-2026.geojson"))
# Liste der verfügbaren Regionen
regions = rlp_regions["name"].unique().tolist() 

for kreis in regions:
    # Filtere Zensus-Daten für den aktuellen Landkreis
    zensus_kreis = rlp_regions[rlp_regions["name"] == kreis]

    # Lade OSM-Straßen für den Landkreis (Bounding Box aus Zensus-Daten)
    bbox = zensus_kreis.total_bounds
    roads = ox.graph_from_bbox(bbox, network_type="drive")
    roads = ox.graph_to_gdfs(roads, nodes=False, edges=True)
    roads = roads.to_crs(zensus_kreis.crs)

    # Räumlicher Join
    joined = gpd.sjoin(roads, zensus_kreis, predicate="intersects")

    # Speichere das Ergebnis
    joined.to_file(os.path.join(data_path, f"strassen_{kreis.lower().replace(" ", "_")}.gpkg"), driver="GPKG")

# Zentroide der Rasterzellen berechnen
gdf["geometry"] = gdf.centroid

# Heatmap-Daten erstellen
heatmap_data = []
for _, row in gdf.iterrows():
    heatmap_data.append({
        "lat": row.geometry.y,
        "lng": row.geometry.x,
        "value": row["prediction2"]
    })

# Speichern als JSON
import json
with open("heatmap_data.json", "w") as f:
    json.dump(heatmap_data, f)