import pandas as pd
import geopandas as gpd
import pystatis as pystat

# Der Anfang ist analog zu data_editing_absolut.py

# Ergebnisse der BTW 2025 fuer Landkreise
btw25_ergebnis_kreis = pd.read_csv("btw2025kreis.csv", header=4, delimiter=";")
# Ergebnisse liegen nur absolut vor
btw25_ergebnis_kreis["GRÜNE - Zweitstimmen_Anteil"] = btw25_ergebnis_kreis["GRÜNE - Zweitstimmen"] / btw25_ergebnis_kreis["Gültige - Zweitstimmen"]

# Lade die Daten, die auf Ebene des 1-qkm-Grids vorliegen
zensus_1km = gpd.read_file("Zensus2022_grid_final_6219414353666344919/Zensus2022_1kmGitter.shp")
# Spaltennamen sind unguenstig, holen wir uns weiter unten besser verstaendlich
zensus_1km.drop(['Einwohner', 'Durchschni', 'DurchschnH',
       'durchschnM', 'durchschnF', 'durchsch_1', 'Eigentueme', 'Leerstands',
       'MALeerstQu', 'Insgesamt_', 'Gas', 'Heizoel', 'Holz_Holzp',
       'Biomasse_B', 'Solar_Geot', 'Strom', 'Kohle', 'Fernwaerme',
       'kein_Energ', 'Insgesamt1', 'Fernheizun', 'Etagenheiz', 'Blockheizu',
       'Zentralhei', 'Einzel_Meh', 'keine_Heiz', 'Unter18', 'a18bis29',
       'a30bis49', 'a50bis64', 'a65undaelt', 'AnteilUebe', 'AnteilUnte',
       'AnteilAusl', 'Insgesam_1', 'Vor1919', 'a1919bis19', 'a1949bis19',
       'a1979bis19', 'a1991bis20', 'a2001bis20', 'a2011bis20', 'a2020undsp'], axis=1, inplace=True)
zensus_1km_df = pd.read_csv("Zensus2022_grid_final_227080922168339922.csv", header=0, delimiter=",")



#########################################################
################# Landkreise ############################
#########################################################
# Spaltennamen im zensus_1km_df:

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
    ['Stichtag', ars, 'Personen__%']], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Personen__%": "Personen unter 18 Jahren"}, inplace=True, axis=1)
zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Alter (5 Altersklassen)"] == "18 bis 29 Jahre",
    ['Stichtag', ars, 'Personen__%']], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Personen__%": "Personen 18 - 29 Jahre"}, inplace=True, axis=1)
zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Alter (5 Altersklassen)"] == "30 bis 49 Jahre",
    ['Stichtag', ars, 'Personen__%']], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Personen__%": "Personen 30 - 49 Jahre"}, inplace=True, axis=1)
zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Alter (5 Altersklassen)"] == "50 bis 64 Jahre",
    ['Stichtag', ars, 'Personen__%']], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Personen__%": "Personen 50 - 64 Jahre"}, inplace=True, axis=1)
zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Alter (5 Altersklassen)"] == "65 Jahre und älter",
    ['Stichtag', ars, 'Personen__%']], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Personen__%": "Personen 65 Jahre und älter"}, inplace=True, axis=1)

# Auslaender
tabelle = pystat.Table(name=codes_zensus_tables[1])
tabelle.get_data(regionalvariable="GEOLK4")
zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Staatsangehörigkeit"] == 'Ausland und Sonstige',
                                                             ["Stichtag", ars, "Personen__%"]], on=[ars, "Stichtag"] )
zensus_landkreise.rename({"Personen__%": "Ausländeranteil"}, inplace=True, axis=1)

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
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__%"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__%": "Blockheizung"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data.Heizungsart == "Etagenheizung", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__%"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__%": "Etagenheizung"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data.Heizungsart == "Fernheizung (Fernwärme)", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__%"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__%": "Fernheizung"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data.Heizungsart == "Einzel-/Mehrraumöfen (auch Nachtspeicherheizung)", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__%"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__%": "Einzel-/ Mehrraumöfen"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data.Heizungsart == "Keine Heizung im Gebäude oder in den Wohnungen", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__%"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__%": "keine Heizung"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data.Heizungsart == "Zentralheizung", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__%"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__%": "Zentralheizung"}, inplace=True, axis=1)

# Wohnungen - Energietraeger
tabelle = pystat.Table(name=codes_zensus_tables[5])
tabelle.get_data(regionalvariable="GEOLK4")

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Energieträger der Heizung"] == "Fernwärme (verschiedene Energieträger)", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__%"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__%": "Fernwärme"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Energieträger der Heizung"] == "Gas", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__%"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__%": "Gas"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Energieträger der Heizung"] == "Holz, Holzpellets", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__%"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__%": "Holz/Holzpellets"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Energieträger der Heizung"] == "Heizöl", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__%"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__%": "Heizöl"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Energieträger der Heizung"] == "Kohle", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__%"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__%": "Kohle"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Energieträger der Heizung"] == "Solar-/Geothermie, Wärmepumpen", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__%"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__%": "Solar/Geothermie/Wärmepumpe"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Energieträger der Heizung"] == "Strom (ohne Wärmepumpe)", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__%"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__%": "Strom"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Energieträger der Heizung"] == "Kein Energieträger (keine Heizung)", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__%"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__%": "kein Energieträger"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Energieträger der Heizung"] == "Biomasse (ohne Holz), Biogas", 
                                                             ["Stichtag", ars, "Wohnungen in Gebäuden mit Wohnraum__%"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Wohnungen in Gebäuden mit Wohnraum__%": "Biomasse/Biogas"}, inplace=True, axis=1)


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
                                                             ["Stichtag", ars, "Gebäude mit Wohnraum__%"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Gebäude mit Wohnraum__%": "Gebäude vor 1919"}, inplace=True, axis=1)

zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Baujahr (Mikrozensus-Klassen)"] == "1919 - 1948", 
                                                             ["Stichtag", ars, "Gebäude mit Wohnraum__%"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Gebäude mit Wohnraum__%": "Gebäude ab 1919 bis 1948"}, inplace=True, axis=1)


zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Baujahr (Mikrozensus-Klassen)"] == "1949 - 1978", 
                                                             ["Stichtag", ars, "Gebäude mit Wohnraum__%"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Gebäude mit Wohnraum__%": "Gebäude ab 1949 bis 1978"}, inplace=True, axis=1)


zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Baujahr (Mikrozensus-Klassen)"] == "1979 - 1990", 
                                                             ["Stichtag", ars, "Gebäude mit Wohnraum__%"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Gebäude mit Wohnraum__%": "Gebäude ab 1979 bis 1990"}, inplace=True, axis=1)


zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Baujahr (Mikrozensus-Klassen)"] == "1991 - 2000", 
                                                             ["Stichtag", ars, "Gebäude mit Wohnraum__%"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Gebäude mit Wohnraum__%": "Gebäude ab 1991 bis 2000"}, inplace=True, axis=1)


zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Baujahr (Mikrozensus-Klassen)"] == "2001 - 2010", 
                                                             ["Stichtag", ars, "Gebäude mit Wohnraum__%"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Gebäude mit Wohnraum__%": "Gebäude ab 2001 bis 2010"}, inplace=True, axis=1)


zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Baujahr (Mikrozensus-Klassen)"] == "2011 - 2019", 
                                                             ["Stichtag", ars, "Gebäude mit Wohnraum__%"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Gebäude mit Wohnraum__%": "Gebäude ab 2011 bis 2019"}, inplace=True, axis=1)


zensus_landkreise = zensus_landkreise.merge(tabelle.data.loc[tabelle.data["Baujahr (Mikrozensus-Klassen)"] == "2020 und später", 
                                                             ["Stichtag", ars, "Gebäude mit Wohnraum__%"]], on=[ars, "Stichtag"])
zensus_landkreise.rename({"Gebäude mit Wohnraum__%": "Gebäude ab 2020 und später"}, inplace=True, axis=1)


# Flaeche (Einwohnerdichte)
tabelle = pystat.Table(name="1000A-0001")
tabelle.get_data()

df = tabelle.data[[ars, "Stichtag", "Fläche__qkm"]]
df[ars] = df[ars].apply(lambda x: int(x[1:5]))
df = df.groupby(ars)["Fläche__qkm"].sum().to_frame()

zensus_landkreise[ars] = zensus_landkreise[ars].astype(int)
zensus_landkreise = zensus_landkreise.merge(df, on=[ars], how="left")
zensus_landkreise["Einwohnerdichte"] = zensus_landkreise["Einwohner"] / zensus_landkreise["Fläche__qkm"]
zensus_1km_df["Einwohnerdichte"] = zensus_1km_df["Einwohner"]


# Die 1km-Grid-Daten muessen teils noch normalisiert werden
cols = ['Gas', 'Heizöl', 'Holz/Holzpellets',
       'Biomasse/Biogas', 'Solar/Geothermie/Wärmepumpe', 'Strom', 'Kohle',
       'Fernwärme', 'kein Energieträger']
for col in cols:
    summe = zensus_1km_df[cols].sum(axis=1)
    summe[summe == 0] = 1
    zensus_1km_df[col] = zensus_1km_df[col]/summe
    zensus_landkreise[col] = zensus_landkreise[col]/100.0 

cols = ['Fernheizung', 'Etagenheizung', 'Blockheizung', 'Zentralheizung',
       'Einzel-/ Mehrraumöfen', 'keine Heizung']
for col in cols:
    summe = zensus_1km_df[cols].sum(axis=1)
    summe[summe == 0] = 1
    zensus_1km_df[col] = zensus_1km_df[col]/summe
    zensus_landkreise[col] = zensus_landkreise[col]/100.0 

cols = ['Gebäude vor 1919',
       'Gebäude ab 1919 bis 1948', 'Gebäude ab 1949 bis 1978',
       'Gebäude ab 1979 bis 1990', 'Gebäude ab 1991 bis 2000',
       'Gebäude ab 2001 bis 2010', 'Gebäude ab 2011 bis 2019',
       'Gebäude ab 2020 und später']
for col in cols:
    summe = zensus_1km_df[cols].sum(axis=1)
    summe[summe == 0] = 1
    zensus_1km_df[col] = zensus_1km_df[col]/summe
    zensus_landkreise[col] = zensus_landkreise[col]/100.0 

cols = ['Personen unter 18 Jahren',
       'Personen 18 - 29 Jahre', 'Personen 30 - 49 Jahre',
       'Personen 50 - 64 Jahre', 'Personen 65 Jahre und älter']
for col in cols:
    summe = zensus_1km_df[cols].sum(axis=1)
    summe[summe == 0] = 1
    zensus_1km_df[col] = zensus_1km_df[col]/summe
    zensus_landkreise[col] = zensus_landkreise[col]/100.0 


zensus_landkreise["Leerstandsquote"] = zensus_landkreise["Leerstandsquote"]/100.0 
zensus_landkreise["Eigentümerquote"] = zensus_landkreise["Eigentümerquote"]/100.0 
zensus_landkreise["Ausländeranteil"] = zensus_landkreise["Ausländeranteil"]/100.0 
zensus_1km_df["Leerstandsquote"] = zensus_1km_df["Leerstandsquote"]/100.0 
zensus_1km_df["Eigentümerquote"] = zensus_1km_df["Eigentümerquote"]/100.0
zensus_1km_df["Ausländeranteil"] = zensus_1km_df["Ausländeranteil"]/100.0


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

zensus_1km_rlp = zensus_1km.clip(rheinland_pfalz)
zensus_landkreise_rlp = zensus_landkreise_geo.clip(rheinland_pfalz)
del zensus_1km
zensus_1km_rlp.set_index("id")
zensus_1km_df.set_index("id")
zensus_1km_rlp = zensus_1km_rlp.merge(zensus_1km_df, on="id")

zensus_landkreise_geo.rename({"GRÜNE - Zweitstimmen_Anteil": "GRUENE_Anteil"}, axis = 1, inplace = True)
zensus_landkreise_geo.rename({"GRÜNE - Zweitstimmen": "GRUENE"}, axis = 1, inplace = True)

zensus_landkreise_geo.to_file("editing_ergebnis/zensus_landkreise_anteile.gpkg", driver="GPKG")
zensus_1km_rlp.to_file("editing_ergebnis/zensus_1km_rlp_anteile.gpkg", driver="GPKG")
final_landkreise.to_csv("editing_ergebnis/Zensus2022_Landkreise.csv")



