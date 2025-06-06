import json
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
import os
from traitement.pretraitement import charger_donnees, pretraiter

# Paramètres
VILLES = ["Douala"]
SEQUENCE_LENGTH = 16
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
MODEL_PATH = os.path.join(DATA_DIR, "modele_lstm.h5")
PREVISIONS_PATH = os.path.join(DATA_DIR, "previsions.json")

# Charger modèle
model = load_model(MODEL_PATH)

all_previsions = {}
for ville in VILLES:
    df = charger_donnees(ville)
    X, _, scaler = pretraiter(df)
    seq = X[-1:].copy()
    preds = []
    for _ in range(SEQUENCE_LENGTH):
        p = model.predict(seq)
        preds.append(p.flatten())
        seq = np.concatenate([seq[:,1:,:], p.reshape(1,1,-1)], axis=1)
    preds_rescaled = scaler.inverse_transform(preds)
    dates = pd.date_range(start=df.index[-1], periods=SEQUENCE_LENGTH+1, freq='3H')[1:]

    liste = []
    for dt, val in zip(dates, preds_rescaled):
        liste.append({
            "date": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "temperature": float(val[0]),
            "pression": float(val[1]),
            "humidite": float(val[2]),
            "vent": float(val[3])
        })
    all_previsions[ville] = liste

with open(PREVISIONS_PATH, 'w', encoding='utf-8') as f:
    json.dump(all_previsions, f, ensure_ascii=False, indent=2)

print(f"✅ Prévisions écrites dans {PREVISIONS_PATH}")