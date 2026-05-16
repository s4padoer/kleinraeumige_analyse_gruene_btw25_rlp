import geopandas as gpd
import os
import pandas as pd
import osmnx as ox
import json
from tobler.area_weighted import area_interpolate

data_path = os.path.join(os.path.dirname(__file__), "data")

# GeoJSON-Daten laden
gdf = gpd.read_file(os.path.join(data_path, "zensus_1km_rlp_with_predictions.geojson"))


## Strassenzuege abspeichern, um das Laden zu reduzieren:
# Lade die Verwaltungsgrenzen von RLP
rlp_regions = gpd.read_file(os.path.join(data_path, "kreise-rlp-2026.geojson"))
# Liste der verfügbaren Regionen
regions = rlp_regions["name"].unique().tolist() 

if rlp_regions.crs != "EPSG:4326":
    rlp_regions = rlp_regions.to_crs("EPSG:4326")
    print("Umgewandeltes CRS:", rlp_regions.crs) 

if gdf.crs != "EPSG:4326":
    gdf = gdf.to_crs("EPSG:4326")
    print("Umgewandeltes CRS:", gdf.crs) 

test2 = area_interpolate(gdf, gdf, intensive_variables=["prediction2"])


zensus_with_landkreis = gpd.sjoin(
    test2,
    rlp_regions,
    predicate="intersects",  # oder "intersects", falls Rasterzellen an Kreisgrenzen liegen
    how="left"  # Behalte alle Rasterzellen, auch wenn sie keinem Landkreis zugeordnet sind
)

# Falls das CRS nicht EPSG:4326 ist, umwandeln
if zensus_with_landkreis.crs != "EPSG:4326":
    zensus_with_landkreis = zensus_with_landkreis.to_crs("EPSG:4326")
    print("Umgewandeltes CRS:", zensus_with_landkreis.crs) 

zensus_with_landkreis.rename({"index_right": "index"}, axis=1, inplace = True)
zensus_with_landkreis[['prediction2', 'geometry', 'index', 'objectid', 'region', 'code',
       'name', 'de_entity', 'fr_entity', 'en_entity', 'fourcolor']].to_file(os.path.join(data_path, "landkreise_with_predictions.geojson"), driver="GeoJSON")


for kreis in regions:
    # Filtere Zensus-Daten für den aktuellen Landkreis
    zensus_kreis = zensus_with_landkreis[zensus_with_landkreis["name"] == kreis]

    # Lade OSM-Straßen für den Landkreis (Bounding Box aus Zensus-Daten)
    bbox = zensus_kreis.total_bounds
    roads = ox.graph_from_bbox(bbox, network_type="drive")
    roads = ox.graph_to_gdfs(roads, nodes=False, edges=True)
    roads = roads.to_crs(zensus_kreis.crs)

    # Räumlicher Join
    joined = gpd.sjoin(roads, zensus_kreis, predicate="intersects")
    
    # Speichere das Ergebnis
    joined.to_file(os.path.join(data_path, f"strassen_{kreis.lower().replace(" ", "_")}.geojson"), driver="GeoJSON")
