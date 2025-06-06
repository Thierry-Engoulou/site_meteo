import folium
import pandas as pd

# Charger les données Excel
df = pd.read_excel("C:\\Users\\RODRIGUE SINGOR\\Desktop\\mon site\\site_projet_fin_etude\\back-end\\data\\meteo_douala4.xlsx")


# Vérifie que les colonnes Latitude/Longitude existent
if "Latitude" not in df.columns or "Longitude" not in df.columns:
    raise ValueError("Le fichier Excel doit contenir les colonnes 'Latitude' et 'Longitude'.")

# Créer une carte centrée sur le Cameroun (coordonnées approximatives du centre du Cameroun)
carte = folium.Map(location=[4.5, 12.5], zoom_start=7)

# Ajouter les points météo
for i, row in df.iterrows():
    popup = f"""
    📅 {row['Date et Heure']}<br>
    🌡️ Temp: {row['Température (°C)']}°C<br>
    💧 Humidité: {row['Humidité (%)']}%<br>
    🌧️ Précipitation: {row['Précipitation (mm)']} mm
    """
    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=5 + row["Précipitation (mm)"] * 2,
        color="blue",
        fill=True,
        fill_color="blue",
        fill_opacity=0.6,
        popup=popup
    ).add_to(carte)

# Enregistrer dans un fichier HTML
carte.save("carte_meteo_cameroun.html")
print("✅ Carte générée avec succès : carte_meteo_cameroun.html")
