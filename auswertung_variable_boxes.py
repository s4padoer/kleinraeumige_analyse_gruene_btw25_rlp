from statsmodels.othermod import betareg
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from sklearn.preprocessing import OneHotEncoder
import matplotlib as mpl
from tobler.model import glm
from tobler.area_weighted import area_interpolate
from tobler.pycno import pycno_interpolate

import folium 
from folium.features import GeoJsonTooltip
import branca.colormap as cm
import contextily as ctx
from pyrosm import get_data, OSM
import matplotlib.colors as colors


# Laden der Daten, die wir in data_editing_absolut.py 
# bzw. _anteile.py zusammengestellt haben

# Landkreis-Struktur
zensus_landkreise_geo = gpd.read_file("editing_ergebnis/zensus_landkreise_anteile.gpkg")
# 1-qkm-Grid
zensus_1km_rlp = gpd.read_file("editing_ergebnis/zensus_1km_rlp_anteile.gpkg")
zensus_1km_df = pd.read_csv("editing_ergebnis/Zensus2022_Landkreise.csv")

rheinland_pfalz = gpd.read_file("SHP_BTW2025/23_LK_1_BTW2025.shp")
rheinland_pfalz.to_crs(zensus_1km_rlp.crs, inplace=True)

zensus_landkreise_rlp = zensus_landkreise_geo.clip(rheinland_pfalz)

# Wir machen noch eine foward-selection, um ggfs. noch ein besseres Modell zu erhalten:

def forward_selection(X, y, criterion='bic'):
    included = []
    remaining = list(X.columns)
    best_score = float('inf')
    best_model = None
    while remaining:
        scores_with_candidates = []
        models = []
        for candidate in remaining:
            model = betareg.BetaModel(endog = y, 
                        exog = X[included + [candidate]], 
                        exog_precision= np.ones((len(y),1)))
            results = model.fit()
            score = getattr(results, criterion)
            scores_with_candidates.append((score, candidate))
            models.append(results)
        idx = np.argsort([x for (x,y) in scores_with_candidates])
        best_new_score, best_candidate = scores_with_candidates[idx[0]]
        if best_new_score < best_score:
            included.append(best_candidate)
            remaining.remove(best_candidate)
            best_score = best_new_score
            best_model = models[idx[0]]
        else:
            break
    return included, best_model

def backward_selection(X, y, criterion='bic'):
    included = list(X.columns)
    best_score = float('inf')
    best_model = None
    while True:
        scores_with_candidates = []
        models = []
        for combo in [included[:i] + included[i+1:] for i in range(len(included))]:
            if not combo:
                continue
            model = betareg.BetaModel(endog = y, 
                        exog = X[combo], 
                        exog_precision= np.ones((len(y),1)))
            results = model.fit()
            score = getattr(results, criterion)
            scores_with_candidates.append((score, combo))
            models.append(results)
        if not scores_with_candidates:
            break
        idx = np.argsort([x for (x,y) in scores_with_candidates])
        scores_with_candidates.sort()
        best_new_score, best_combo = scores_with_candidates[0]
        if best_new_score < best_score:
            included = best_combo
            best_score = best_new_score
            best_model = models[idx[0]]
        else:
            break
    return included, best_model


covariates = ['Einwohnerdichte', 'Personen unter 18 Jahren', 'Personen 18 - 29 Jahre',
       'Personen 30 - 49 Jahre', 'Personen 50 - 64 Jahre',
       'Personen 65 Jahre und älter', 'Ausländeranteil',
       'Durchschnittliche Haushaltsgröße',
       'Durchschnittliche Nettokaltmiete/qm', 'Blockheizung', 'Etagenheizung',
       'Fernheizung', 'Einzel-/ Mehrraumöfen', 'keine Heizung',
       'Zentralheizung', 'Fernwärme', 'Gas', 'Holz/Holzpellets', 'Heizöl',
       'Kohle', 'Solar/Geothermie/Wärmepumpe', 'Strom', 'kein Energieträger',
       'Biomasse/Biogas', 'Leerstandsquote', 'Eigentümerquote',
       'Gebäude vor 1919', 'Gebäude ab 1919 bis 1948',
       'Gebäude ab 1949 bis 1978', 'Gebäude ab 1979 bis 1990',
       'Gebäude ab 1991 bis 2000', 'Gebäude ab 2001 bis 2010',
       'Gebäude ab 2011 bis 2019', 'Gebäude ab 2020 und später']

ars = 'Amtlicher Regionalschlüssel (ARS)__Code'
colinear = ['Personen unter 18 Jahren', 'keine Heizung', 'kein Energieträger', 'Gebäude vor 1919']
for var in colinear:
    covariates.remove(var)

many_nas = ["Kohle", "Biomasse/Biogas"]
for var in many_nas:
    covariates.remove(var)

log_covariates = []
for var in covariates:
    name = "log " + var
    col = zensus_landkreise_geo[var]
    zensus_landkreise_geo[name] = np.log( col + 0.00001 )
    col = zensus_1km_rlp[var]
    zensus_1km_rlp[name] = np.log( col + 0.00001)
    log_covariates.append(name)



df = zensus_landkreise_geo[covariates+log_covariates+["GRUENE_Anteil",ars]].dropna()
encoder = OneHotEncoder(sparse_output=False,min_frequency=7).fit(zensus_landkreise_geo[[ars]] // 1000)
encoded = encoder.transform(df[[ars]] // 1000)
encoded_rlp = encoder.transform(np.ones((zensus_1km_rlp.shape[0],1))*7) # hier gibt es ein paar Ungenaugikeiten, das betrifft aber

X = pd.DataFrame( np.concat([encoded, df[log_covariates+covariates]], axis = 1) )
X_rlp = pd.DataFrame( np.concat([encoded_rlp, zensus_1km_rlp[log_covariates+covariates]], axis=1))

colnames = [f"bundesland_{x}" for x in range(encoded.shape[1])] + log_covariates+covariates
X.columns = colnames
X_rlp.columns = colnames
covariates_optimal, best_model = backward_selection(X, df["GRUENE_Anteil"].to_numpy())
covariates_optimal2, best_model2 = forward_selection(X, df["GRUENE_Anteil"].to_numpy())

print(best_model.summary(xname=["intercept"]+covariates_optimal))
print(best_model2.summary(xname=["intercept"]+covariates_optimal2))


zensus_1km_rlp["prediction"] = best_model.predict(
    exog_precision=np.ones((zensus_1km_rlp.shape[0],1)),
    exog=X_rlp[covariates_optimal])
test = area_interpolate(zensus_1km_rlp, zensus_1km_rlp, intensive_variables=["prediction"])
test.plot(column="prediction")

zensus_1km_rlp["prediction2"] = best_model2.predict(
    exog_precision=np.ones((zensus_1km_rlp.shape[0],1)),
    exog=X_rlp[covariates_optimal2])
test2 = area_interpolate(zensus_1km_rlp, zensus_1km_rlp, intensive_variables=["prediction2"])
test2.plot(column="prediction2")

## Für das Deployment:

zensus_1km_rlp.to_file("deployment/zensus_1km_rlp_with_predictions.geojson", driver="GeoJSON")


#####################################################################################################
#### Darstellung

trier = gpd.read_file("ortsbezirke_trier2.geojson")

bbox_dict = {}
for _, row in trier.iterrows():
    minx, miny, maxx, maxy = row.geometry.bounds
    bbox_dict[row["ORTSBEZIRK"]] = [minx, miny, maxx, maxy]

for name, bbox in bbox_dict.items():
    name = name.replace("/", "_")
    bounds = [[bbox[1], bbox[0]], [bbox[3], bbox[2]]]
    location = np.array(np.asmatrix(bounds).mean(axis = 0)).reshape(-1)

    osm = OSM("rheinland-pfalz-251020.osm.pbf", bounding_box=bbox)
    roads = osm.get_network(network_type="driving") 
    roads = roads.to_crs(zensus_1km_rlp.crs)

    joined = gpd.sjoin(roads, test, predicate='intersects')
    ax = joined.plot(column='prediction', legend=True, linewidth=2, figsize=(10, 10), cmap='viridis', alpha=0.8)

    # OpenStreetMap als Hintergrundkarte hinzufügen
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

    ax.set_axis_off()
    plt.show()


    joined2 = gpd.sjoin(roads, test2, predicate='intersects')
    vmin = joined2['prediction2'].clip(lower=1e-6).min()
    vmax = joined2['prediction2'].max()
    ax2 = joined2.plot(column='prediction2', legend=True, linewidth=2, 
                   figsize=(10, 10), cmap='magma', alpha=0.8)

    # OpenStreetMap als Hintergrundkarte hinzufügen
    ctx.add_basemap(ax2, source=ctx.providers.OpenStreetMap.Mapnik)

    ax2.set_axis_off()
    plt.savefig(f"grafiken/{name}_karte_strassenzuege.png", dpi=300, bbox_inches="tight")
    plt.show()

    ax2 = joined2.plot(column='prediction2', legend=True, 
                   linewidth=2, figsize=(10, 10), cmap='magma', 
                   norm=colors.LogNorm(vmin=vmin, vmax=vmax), alpha=0.8)

    # OpenStreetMap als Hintergrundkarte hinzufügen
    ctx.add_basemap(ax2, source=ctx.providers.OpenStreetMap.Mapnik)

    ax2.set_axis_off()
    plt.savefig(f"grafiken/{name}_karte_strassenzuege_logskala.png", dpi=300, bbox_inches="tight")
    plt.show()

#bbox = [6.63, 49.72, 6.71, 49.79] # Trier
#bbox = [7.55, 50.20, 7.70, 50.30] # Brey, Rhens, Spay und Waldesch
#bbox = [7.50, 50.25, 7.60, 50.30]
#bbox = [6.64, 49.79, 6.73, 49.83] # Ehrang/ Quint

#bounds = [[49.39, 6.1], [50.57, 7.6]] # Trier
#bounds = [[50.20, 7.55], [50.30, 7.70]] # Brey, Rhens, Spay und Waldesch
#bounds = [[50.25, 7.50], [50.30, 7.60]] # Waldesch
#bounds = [[49.79, 6.64], [49.83, 6.73]] # Ehrang/ Quint


################### Bei Bedarf das hier auch in die Loop rein,
################### um zentrierte html-Grafiken zu erstellen
pred = 'prediction2'
m = folium.Map(location=location, zoom_start=8, max_bounds=True)
m.fit_bounds(bounds)

# Erstelle eine Farbskala (colormap) für die Werte zwischen 0 und 1
colormap = cm.LinearColormap(colors=['blue', 'green', 'yellow', 'red'], vmin=0, vmax=1)

# Funktion, um für jeden Eintrag die Farbe nach Attributwert zu bestimmen
def style_function(feature):
    val = feature['properties'][pred]
    return {
        'fillColor': colormap(val),
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.2,
    }

# Füge GeoJSON-Layer mit Tooltip zur Karte hinzu, Tooltip zeigt Attribut beim Hover
tooltip = GeoJsonTooltip(fields=[pred],
                         aliases=['Stimmanteil:'],
                         localize=True)

folium.GeoJson(
    test2,
    style_function=style_function,
    tooltip=tooltip
).add_to(m)

# Füge eine Legende (Colorbar) hinzu
colormap.caption = 'Geschätzter Stimmanteil - GRÜNE'
colormap.add_to(m)

m.save("karte_1km_grid_rlp_automated_selection.html")