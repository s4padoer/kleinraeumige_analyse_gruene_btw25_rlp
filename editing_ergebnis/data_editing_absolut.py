import requests
import pandas as pd
import geopandas as gpd
import pystatis as pystat


# Ergebnisse fuer Landkreise bzw. Wahlkreise
btw25_ergebnis_kreis = pd.read_csv("btw2025kreis.csv", header=4, delimiter=";")
btw25_ergebnis_kreis["GRÜNE - Zweitstimmen_Anteil"] = btw25_ergebnis_kreis["GRÜNE - Zweitstimmen"] / btw25_ergebnis_kreis["Gültige - Zweitstimmen"]

zensus_1km = gpd.read_file("Zensus2022_grid_final_6219414353666344919/Zensus2022_1kmGitter.shp")
zensus_1km.drop(['Einwohner', 'Durchschni', 'DurchschnH',
       'durchschnM', 'durchschnF', 'durchsch_1', 'Eigentueme', 'Leerstands',
       'MALeerstQu', 'Insgesamt_', 'Gas', 'Heizoel', 'Holz_Holzp',
       'Biomasse_B', 'Solar_Geot', 'Strom', 'Kohle', 'Fernwaerme',
       'kein_Energ', 'Insgesamt1', 'Fernheizun', 'Etagenheiz', 'Blockheizu',
       'Zentralhei', 'Einzel_Meh', 'keine_Heiz', 'Unter18', 'a18bis29',
       'a30bis49', 'a50bis64', 'a65undaelt', 'AnteilUebe', 'AnteilUnte',
       'AnteilAusl', 'Insgesam_1', 'Vor1919', 'a1919bis19', 'a1949bis19',
       'a1979bis19', 'a1991bis20', 'a2001bis20', 'a2011bis20', 'a2020undsp'], axis=1, inplace=True)
zensus_1km_df = pd.read_csv("Zensus2022_grid_final_8225047377848191026.csv", header=0, delimiter=",")



#########################################################
################# Landkreise ############################
#########################################################

# Zensus 1km
# Index(['OBJECTID', 'id', 'GITTER_ID_1km', 'Einwohner', 'Durchschnittsalter',
#        'Durchschnittliche Haushaltsgröße',
#        'Durchschnittliche Nettokaltmiete/qm',
#        'Durchschnittliche Fläche je Wohnung ',
#        'Durchschnittliche Fläche je Bewohner', 'Eigentümerquote',
#        'Leerstandsquote', 'Markaktive Leerstandsquote',
#        'Energieträger insgesamt', 'Gas', 'Heizöl', 'Holz/Holzpellets',
#        'Biomasse/Biogas', 'Solar/Geothermie/Wärmepumpe', 'Strom', 'Kohle',
#        'Fernwärme', 'kein Energieträger', 'Heizungsart insgesamt',
#        'Fernheizung', 'Etagenheizung', 'Blockheizung', 'Zentralheizung',
#        'Einzel-/ Mehrraumöfen', 'keine Heizung', 'Personen unter 18 Jahren',
#        'Personen 18 - 29 Jahre', 'Personen 30 - 49 Jahre',
#        'Personen 50 - 64 Jahre', 'Personen 65 Jahre und älter',
#        'Anteil der ab 65-Jährigen', 'Anteil der unter 18-Jährigen',
#        'Ausländeranteil', 'Gebäude insgesamt', 'Gebäude vor 1919',
#        'Gebäude ab 1919 bis 1948', 'Gebäude ab 1949 bis 1978',
#        'Gebäude ab 1979 bis 1990', 'Gebäude ab 1991 bis 2000',
#        'Gebäude ab 2001 bis 2010', 'Gebäude ab 2011 bis 2019',
#        'Gebäude ab 2020 und später', 'Shape__Area', 'Shape__Length',
#        'Flaeche'],
#       dtype='object') 


codes_zensus_tables = ["1000A-1003", "1000A-1019", 
                       "5000H-0001", "5000H-0005", "4000W-1015",
                       "4000W-1012", "4000W-0001", 
                       "3000G-1004"]

# Daten fuer Landkreise aus Zensusdatenbank
# Einwohner
tabelle = pystat.Table(name=codes_zensus_tables[0])
tabelle.get_data(regionalvariable="GEOLK4")

ars = 'Amtlicher Regionalschlüssel (ARS)__Code'
zensus_landkreise = tabelle.data.loc[tabelle.data["Alter (5 Altersklassen)"] == "Insgesamt",
    ['Stichtag', ars, 'Personen__Anzahl']]
zensus_landkreise.rename({'Personen__Anzahl': "Einwohner"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Alter (5 Altersklassen)"] == "Unter 18 Jahre",
    ['Stichtag', ars, 'Personen__Anzahl']], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Personen__Anzahl": "Personen unter 18 Jahren"}, inplace=True, axis=1)
zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Alter (5 Altersklassen)"] == "18 bis 29 Jahre",
    ['Stichtag', ars, 'Personen__Anzahl']], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Personen__Anzahl": "Personen 18 - 29 Jahre"}, inplace=True, axis=1)
zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Alter (5 Altersklassen)"] == "30 bis 49 Jahre",
    ['Stichtag', ars, 'Personen__Anzahl']], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Personen__Anzahl": "Personen 30 - 49 Jahre"}, inplace=True, axis=1)
zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Alter (5 Altersklassen)"] == "50 bis 64 Jahre",
    ['Stichtag', ars, 'Personen__Anzahl']], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Personen__Anzahl": "Personen 50 - 64 Jahre"}, inplace=True, axis=1)
zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Alter (5 Altersklassen)"] == "65 Jahre und älter",
    ['Stichtag', ars, 'Personen__Anzahl']], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Personen__Anzahl": "Personen 65 Jahre und älter"}, inplace=True, axis=1)

# Auslaender
tabelle = pystat.Table(name=codes_zensus_tables[1])
tabelle.get_data(regionalvariable="GEOLK4")
zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Staatsangehörigkeit"] == 'Ausland und Sonstige',
                                                             ["Stichtag", ars, "Personen__Anzahl"]], on=[ars, "Stichtag"] )
zensus_landkreise.rename({"Personen__Anzahl": "Ausländeranteil"}, inplace=True, axis=1)

# Haushalte
tabelle = pystat.Table(name=codes_zensus_tables[2])
tabelle.get_data(regionalvariable="GEOLK4")
zensus_landkreise = zensus_landkreise.merge(tabelle.data[["Stichtag", ars, "Durchschnittliche Haushaltsgröße__Personen"]], 
                                            on=[ars, "Stichtag"], how="left")
zensus_landkreise.rename({"Durchschnittliche Haushaltsgröße__Personen": "Durchschnittliche Haushaltsgröße"}, inplace=True, axis=1)

tabelle = pystat.Table(name=codes_zensus_tables[3])
tabelle.get_data(regionalvariable="GEOLK4")
zensus_landkreise = zensus_landkreise.merge(tabelle.data[["Stichtag", ars, "Durchschnittliche Nettokaltmiete je Haushalt__€/m²"]], 
                                            on=[ars, "Stichtag"], how="left")
zensus_landkreise.rename({"Durchschnittliche Nettokaltmiete je Haushalt__€/m²": "Durchschnittliche Nettokaltmiete/qm"}, inplace=True, axis=1)

# Wohnungen - Heizungsart
tabelle = pystat.Table(name=codes_zensus_tables[4])
tabelle.get_data(regionalvariable="GEOLK4")

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data.Heizungsart == "Blockheizung", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__Anzahl"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__Anzahl": "Blockheizung"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data.Heizungsart == "Etagenheizung", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__Anzahl"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__Anzahl": "Etagenheizung"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data.Heizungsart == "Fernheizung (Fernwärme)", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__Anzahl"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__Anzahl": "Fernheizung"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data.Heizungsart == "Einzel-/Mehrraumöfen (auch Nachtspeicherheizung)", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__Anzahl"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__Anzahl": "Einzel-/ Mehrraumöfen"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data.Heizungsart == "Keine Heizung im Gebäude oder in den Wohnungen", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__Anzahl"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__Anzahl": "keine Heizung"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data.Heizungsart == "Zentralheizung", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__Anzahl"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__Anzahl": "Zentralheizung"}, inplace=True, axis=1)

# Wohnungen - Energietraeger
tabelle = pystat.Table(name=codes_zensus_tables[5])
tabelle.get_data(regionalvariable="GEOLK4")

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Energieträger der Heizung"] == "Fernwärme (verschiedene Energieträger)", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__Anzahl"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__Anzahl": "Fernwärme"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Energieträger der Heizung"] == "Gas", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__Anzahl"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__Anzahl": "Gas"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Energieträger der Heizung"] == "Holz, Holzpellets", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__Anzahl"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__Anzahl": "Holz/Holzpellets"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Energieträger der Heizung"] == "Heizöl", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__Anzahl"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__Anzahl": "Heizöl"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Energieträger der Heizung"] == "Kohle", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__Anzahl"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__Anzahl": "Kohle"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Energieträger der Heizung"] == "Solar-/Geothermie, Wärmepumpen", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__Anzahl"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__Anzahl": "Solar/Geothermie/Wärmepumpe"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Energieträger der Heizung"] == "Strom (ohne Wärmepumpe)", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__Anzahl"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__Anzahl": "Strom"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Energieträger der Heizung"] == "Kein Energieträger (keine Heizung)", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__Anzahl"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__Anzahl": "kein Energieträger"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Energieträger der Heizung"] == "Biomasse (ohne Holz), Biogas", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__Anzahl"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__Anzahl": "Biomasse/Biogas"}, inplace=True, axis=1)


tabelle = pystat.Table(name=codes_zensus_tables[6])
tabelle.get_data(regionalvariable="GEOLK4")


zensus_landkreise = zensus_landkreise.merge(tabelle.data[["Stichtag", ars, "Leerstandsquote__%"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Leerstandsquote__%": "Leerstandsquote"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data[["Stichtag", ars, "Eigentumsquote__%"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Eigentumsquote__%": "Eigentümerquote"}, inplace=True, axis=1)

# Gebaeude
tabelle = pystat.Table(name=codes_zensus_tables[7])
tabelle.get_data(regionalvariable="GEOLK4")

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Baujahr (Mikrozensus-Klassen)"] == "Vor 1919", 
                                                             ["Stichtag", ars, "Gebäude mit Wohnraum__Anzahl"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Gebäude mit Wohnraum__Anzahl": "Gebäude vor 1919"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Baujahr (Mikrozensus-Klassen)"] == "1919 - 1948", 
                                                             ["Stichtag", ars, "Gebäude mit Wohnraum__Anzahl"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Gebäude mit Wohnraum__Anzahl": "Gebäude ab 1919 bis 1948"}, inplace=True, axis=1)


zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Baujahr (Mikrozensus-Klassen)"] == "1949 - 1978", 
                                                             ["Stichtag", ars, "Gebäude mit Wohnraum__Anzahl"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Gebäude mit Wohnraum__Anzahl": "Gebäude ab 1949 bis 1978"}, inplace=True, axis=1)


zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Baujahr (Mikrozensus-Klassen)"] == "1979 - 1990", 
                                                             ["Stichtag", ars, "Gebäude mit Wohnraum__Anzahl"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Gebäude mit Wohnraum__Anzahl": "Gebäude ab 1979 bis 1990"}, inplace=True, axis=1)


zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Baujahr (Mikrozensus-Klassen)"] == "1991 - 2000", 
                                                             ["Stichtag", ars, "Gebäude mit Wohnraum__Anzahl"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Gebäude mit Wohnraum__Anzahl": "Gebäude ab 1991 bis 2000"}, inplace=True, axis=1)


zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Baujahr (Mikrozensus-Klassen)"] == "2001 - 2010", 
                                                             ["Stichtag", ars, "Gebäude mit Wohnraum__Anzahl"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Gebäude mit Wohnraum__Anzahl": "Gebäude ab 2001 bis 2010"}, inplace=True, axis=1)


zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Baujahr (Mikrozensus-Klassen)"] == "2011 - 2019", 
                                                             ["Stichtag", ars, "Gebäude mit Wohnraum__Anzahl"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Gebäude mit Wohnraum__Anzahl": "Gebäude ab 2011 bis 2019"}, inplace=True, axis=1)


zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Baujahr (Mikrozensus-Klassen)"] == "2020 und später", 
                                                             ["Stichtag", ars, "Gebäude mit Wohnraum__Anzahl"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Gebäude mit Wohnraum__Anzahl": "Gebäude ab 2020 und später"}, inplace=True, axis=1)

# Flaeche (Einwohnerdichte)
tabelle = pystat.Table(name="1000A-0001")
tabelle.get_data()

df = tabelle.data[[ars, "Stichtag", "Fläche__qkm"]]
df[ars] = df[ars].apply(lambda x: int(x[1:5]))
df = df.groupby(ars)["Fläche__qkm"].sum().to_frame()

zensus_landkreise[ars] = zensus_landkreise[ars].astype(int)
zensus_landkreise = zensus_landkreise.merge(df, on=[ars], how="left")
zensus_landkreise["Einwohnerdichte"] = zensus_landkreise["Einwohner"] / zensus_landkreise["Fläche__qkm"]
zensus_1km_df["Einwohnerdichte"] = zensus_1km_df.Einwohner



zensus_landkreise.to_csv("editing_ergebnis/Zensus2022_Landkreise_absolut.csv")
zensus_landkreise = pd.read_csv("editing_ergebnis/Zensus2022_Landkreise_absolut.csv")


# Weg wegen Multikollinearitaet:
colinear = ['Personen unter 18 Jahren', 'keine Heizung', 'keine Energieträger', 'Gebäude vor 1919']

cols_regression = {x for x in zensus_1km_df.columns.to_list()}
cols_regression = cols_regression & {x for x in zensus_landkreise.columns.to_list()}
cols_regression = cols_regression.difference(colinear)
cols_regression = list(cols_regression)

final_landkreise = zensus_landkreise.merge(btw25_ergebnis_kreis[["Statistische Kennziffer", "GRÜNE - Zweitstimmen", "GRÜNE - Zweitstimmen_Anteil"]],
                        left_on= ars, right_on="Statistische Kennziffer")



# Shapefile Landkreise (Zensus)
zensus_landkreise_geo = gpd.read_file("K-2023-AI002-1-5--AI0201--2025-10-26/K-2023-AI002-1-5--AI0201--2025-10-26.shp")
zensus_landkreise_geo[ars] = zensus_landkreise_geo.schluessel.astype(int)

zensus_landkreise_geo = zensus_landkreise_geo.merge(final_landkreise, how="left", on = ars)
zensus_landkreise_geo.drop("Einwohnerdichte", axis=1, inplace=True)
zensus_landkreise_geo.rename({"ai0201": "Einwohnerdichte"}, axis=1, inplace=True)
zensus_landkreise_geo.to_crs(zensus_1km.crs, inplace=True)

rheinland_pfalz = gpd.read_file("SHP_BTW2025/23_LK_1_BTW2025.shp")
rheinland_pfalz.to_crs(zensus_1km.crs, inplace=True)

zensus_landkreise_rlp = zensus_landkreise_geo.clip(rheinland_pfalz)

zensus_1km_rlp = zensus_1km.clip(rheinland_pfalz)
del zensus_1km
zensus_1km_df.drop(["Shape__Area", "Shape__Length"], axis=1, inplace=True)
zensus_1km_rlp.set_index("id", inplace=True)
zensus_1km_df.set_index("id", inplace=True)
zensus_1km_rlp = zensus_1km_rlp.merge(zensus_1km_df, on="id")


zensus_landkreise_geo.to_file("editing_ergebnis/zensus_landkreise_absolut.shp")
zensus_1km_rlp.to_file("editing_ergebnis/zensus_1km_rlp_absolut.shp")

## Analyse
from tobler.model import glm
from tobler.area_weighted import area_interpolate
from tobler.pycno import pycno_interpolate
import matplotlib.pyplot as plt

gruene = "GRÜNE - Zweitstimmen"
gruene_anteil = gruene + "_Anteil"

intensive_cols = ['Durchschnittliche Haushaltsgröße',
       'Durchschnittliche Nettokaltmiete/qm', 'Eigentümerquote',
       'Leerstandsquote', "Einwohnerdichte", gruene_anteil]

extensive_cols = ["Einwohner", 'Gas', 'Heizöl', 'Holz/Holzpellets',
       'Biomasse/Biogas', 'Solar/Geothermie/Wärmepumpe', 'Strom', 'Kohle',
       'Fernwärme', 'kein Energieträger',
       'Fernheizung', 'Etagenheizung', 'Blockheizung', 'Zentralheizung',
       'Einzel-/ Mehrraumöfen', 'keine Heizung', 'Personen unter 18 Jahren',
       'Personen 18 - 29 Jahre', 'Personen 30 - 49 Jahre',
       'Personen 50 - 64 Jahre', 'Personen 65 Jahre und älter',
       'Ausländeranteil', 'Gebäude vor 1919',
       'Gebäude ab 1919 bis 1948', 'Gebäude ab 1949 bis 1978',
       'Gebäude ab 1979 bis 1990', 'Gebäude ab 1991 bis 2000',
       'Gebäude ab 2001 bis 2010', 'Gebäude ab 2011 bis 2019',
       'Gebäude ab 2020 und später', gruene]

test1 = area_interpolate(source_df = zensus_landkreise_rlp, 
                         target_df=zensus_1km_rlp, n_jobs=3, 
                         intensive_variables=intensive_cols,
                         extensive_variables=extensive_cols
                         )


fig, ax = plt.subplots(1,2)
zensus_landkreise_rlp.plot(column=gruene_anteil)
test1.plot(column=gruene_anteil)
plt.show()

test2 = pycno_interpolate(source_df = zensus_landkreise_rlp, 
                         target_df=zensus_1km_rlp, 
                         variables= intensive_cols+extensive_cols, cellsize=1000)

test2.plot(column=gruene_anteil)


import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

src_path = 'rasterdaten/rasterdaten.tif'
dst_path = 'rasterdaten/rasterdaten_reprojected.tif'

import rasterio
with rasterio.open(src_path) as src:
    transform, width, height = calculate_default_transform(
        src.crs, zensus_landkreise_rlp.crs, src.width, src.height, *src.bounds)
    kwargs = src.meta.copy()
    kwargs.update({
        'crs': zensus_landkreise_rlp.crs,
        'transform': transform,
        'width': width,
        'height': height
    })

    with rasterio.open(dst_path, 'w', **kwargs) as dst:
        for i in range(1, src.count + 1):
            reproject(
                source=rasterio.band(src, i),
                destination=rasterio.band(dst, i),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=zensus_landkreise_rlp.crs,
                resampling=Resampling.nearest)
            
with rasterio.open(dst_path) as src:
    shapes=zensus_1km_rlp.geometry.values
    # Maskiere und schneide das Raster zu (crop=True)
    out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)

    # Metadaten anpassen
    out_meta = src.meta.copy()
    out_meta.update({
        "driver": "GTiff",
        "height": out_image.shape[1],
        "width": out_image.shape[2],
        "transform": out_transform
    })

# Speicher das zugeschnittene Raster als neue GeoTIFF
with rasterio.open('rasterdaten/rasterdaten_clipped.tif', "w", **out_meta) as dest:
    dest.write(out_image)

zensus_landkreise_rlp.rename({gruene: "GRUENE_Zweitstimmen"}, inplace=True, axis=1)
zensus_1km_rlp.rename({gruene: "GRUENE_Zweitsteimmen"}, inplace=True, axis=1)

test3, model = glm(source_df = zensus_landkreise_rlp.dropna(), target_df = zensus_1km_rlp.dropna(), variable="GRUENE_Zweitstimmen",
                   raster="rasterdaten/rasterdaten_clipped.tif", likelihood = "poisson", return_model=True)

test3.plot(column="GRUENE_Zweitstimmen")

