from flask import Flask, render_template, request
import pandas as pd
from datetime import datetime, timedelta
import folium

app = Flask(__name__)
EXCEL_PATH = "./data/meteo_douala4.xlsx"


#1er
@app.route("/")
def accueil():
    # Chargement des données depuis le fichier Excel
    df = pd.read_excel(EXCEL_PATH)
    df["Date et Heure"] = pd.to_datetime(df["Date et Heure"])

    # Garder les 48 dernières heures
    maintenant = datetime.now()
    df = df[df["Date et Heure"] >= (maintenant - timedelta(hours=48))]
    df = df.sort_values("Date et Heure")

    # Séries à tracer
    labels = df["Date et Heure"].tolist()
    temps = df["Température (°C)"].tolist()
    humidite = df["Humidité (%)"].tolist()
    pression = df["Pression (hPa)"].tolist()
    vent = df["Vitesse du vent (m/s)"].tolist()

    # Génération de la carte Folium
    carte = folium.Map(location=[4.05, 9.7], zoom_start=12,
                        width="100%",  # s'adapte à la largeur du conteneur
                        height="400px"  # hauteur fixe
    )
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=5 + row["Précipitation (mm)"] * 2,
            color="blue", fill=True, fill_opacity=0.6,
            popup=(
                f"📅 {row['Date et Heure'].strftime('%Y-%m-%d %H:%M')}<br>"
                f"🌡️ {row['Température (°C)']}°C  💧 {row['Humidité (%)']}%<br>"
                f"🌬️ {row['Vitesse du vent (m/s)']} m/s  🌧️ {row['Précipitation (mm)']} mm"
            )
        ).add_to(carte)
    carte_html = carte._repr_html_()

    # Passer toutes les données nécessaires au template
    return render_template(
        "dashboard.html",
        carte_html=carte_html,
        labels=labels,
        temps=temps,
        humidite=humidite,
        pression=pression,
        vent=vent,
        data=df.to_dict(orient="records") # Passer les données brutes pour le filtrage JS
    )

@app.route("/previsions")
def afficher_prevision():
    df = pd.read_excel(EXCEL_PATH)
    df = df.tail(48)  # Dernières 48 entrées (chaque 10 minutes ≈ 8h, ajuster si besoin)
    data = df.to_dict(orient='records')

    # Préparer les données pour le graphique
    labels = df['Date et Heure'].tolist()
    temperatures = df['Température (°C)'].tolist()

    return render_template('prevision.html', data=data, labels=labels, temperatures=temperatures)

#2ieme
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
