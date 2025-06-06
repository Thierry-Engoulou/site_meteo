import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os

# Chemin vers le fichier de collecte
CHEMIN_EXCEL = os.path.join(os.path.dirname(__file__), "..", "data", "meteo_donnees.xlsx")
SEQUENCE_LENGTH = 16  # 48h / 3h


def charger_donnees(ville: str) -> pd.DataFrame:
    df = pd.read_excel(CHEMIN_EXCEL, sheet_name=ville)
    df['Date et Heure'] = pd.to_datetime(df['Date et Heure'])
    df = df.sort_values('Date et Heure')
    df = df.set_index('Date et Heure')
    # Resample à chaque heure (ici données toutes les 10 min -> agrégation 1h)
    df = df.resample('1H').mean().ffill()
    return df


def pretraiter(df: pd.DataFrame):
    # Conserver les colonnes météo
    features = df[['Temperature', 'Pression', 'Humidite', 'Vent']].values
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(features)
    X, y = [], []
    for i in range(len(scaled) - SEQUENCE_LENGTH):
        X.append(scaled[i:i+SEQUENCE_LENGTH])
        y.append(scaled[i+SEQUENCE_LENGTH])
    X = np.array(X)
    y = np.array(y)
    return X, y, scaler