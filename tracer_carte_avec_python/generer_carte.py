import folium
import pandas as pd

# Charger les données Excel
df = pd.read_excel("meteo_douala4.xlsx")

# Vérifie que les colonnes Latitude/Longitude existent
if "Latitude" not in df.columns or "Longitude" not in df.columns:
    raise ValueError("Le fichier Excel doit contenir les colonnes 'Latitude' et 'Longitude'.")

# Créer une carte centrée sur Douala
carte = folium.Map(location=[4.05, 9.7], zoom_start=12)

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
carte.save("./templates/carte_meteo_douala.html")
print("✅ Carte générée avec succès : carte_meteo_douala.html")
