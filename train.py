# train.py
from traitement.pretraitement import charger_donnees, pretraiter
from traitement.modele_lstm import entrainer

def main():
    villes = ['Douala']  # ajoute d'autres villes si tu veux
    for ville in villes:
        print(f"🚀 Entraînement pour {ville}...")
        df = charger_donnees(ville)
        X, y, _ = pretraiter(df)
        entrainer(X, y)
        print(f"✅ Modèle pour {ville} enregistré.\n")

if __name__ == '__main__':
    main()
