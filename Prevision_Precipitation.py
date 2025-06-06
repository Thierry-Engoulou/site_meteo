from flask import Flask, render_template, jsonify
import os

# Importation des prédictions en tenant compte de l'organisation des fichiers
try:
    from scripts.predictions import make_predictions  # Si `predictions.py` est bien dans `scripts`
except ModuleNotFoundError as e:
    print(f"⚠️ Erreur d'import ({e}): `predictions.py` introuvable dans `scripts/`. Vérifiez son emplacement.")
    make_predictions = None  # Empêche un blocage total du serveur Flask

# Définition de l'application Flask
app = Flask(__name__, template_folder="templates")

@app.route("/")
def index():
    """Affichage de la page principale avec les prédictions."""
    try:
        predictions = make_predictions() if make_predictions else {"error": "Module de prédictions indisponible."}
    except Exception as e:
        print(f"⚠️ Erreur lors de la génération des prédictions : {e}")
        predictions = {"error": "Une erreur est survenue lors du calcul des prédictions."}

    return render_template('index2.html', predictions=predictions)

@app.route("/api/previsions")
def api_previsions():
    """Route API pour récupérer les prédictions en JSON."""
    try:
        predictions = make_predictions() if make_predictions else {"error": "Module de prédictions indisponible."}
    except Exception as e:
        print(f"⚠️ Erreur lors de la génération des prédictions : {e}")
        predictions = {"error": "Une erreur est survenue lors du calcul des prédictions."}

    return jsonify(predictions)

if __name__ == "__main__":
    app.run(debug=True)
