# Kleinräumige Analyse des Stimmenanteils der Grünen in Rheinland-Pfalz bei den Bundestagswahlen

Wahlergebnisse der letzten Bundestagswahl (BTW25) liegen zwar als .csv für die einzelnen Stimmbezirke in Rheinland-Pfalz vor, aber der genaue Zuschnitt der Wahlbezirke ist leider nicht bekannt. Daher soll der Wähleranteil (an Zweitstimmen) kleinteilig mithilfe von Zensusdaten (2022) im 1qkm Gitter geschätzt werden.

Die Daten stammen von:
- https://www.wahlen.rlp.de/service/geodaten (für die Shapefiles SHP_BTW2025)
- https://www.wahlen.rlp.de/bundestagswahl/ergebnisse (BTW_2025_*.xlsx)
- https://www.bundeswahlleiterin.de/bundestagswahlen/2025/wahlkreiseinteilung/downloads.html (btw25_gemetrie_wahlkreise_shp_geo)
- https://www.bundeswahlleiterin.de/bundestagswahlen/2025/ergebnisse/weitere-ergebnisse.html (btw25*.csv)
- https://atlas.zensus2022.de/ (fuer die Daten ueber pystat bezogen)
- K-2023-AI002-1-5--AI0201--2025-10-26 : Shapefiles der Landkreise
- https://plattform-npgeo-vfdb.hub.arcgis.com/datasets/esri-de-content::zensus-2022-gitterzellen/explore?layer=1 (für das Zensus2022_grid im .gitignore aufgrund der Datengröße)