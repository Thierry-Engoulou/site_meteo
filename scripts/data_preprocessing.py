import os
import joblib
import pandas as pd
import numpy as np
from zipfile import BadZipFile
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

# Fonction pour détecter le séparateur dans un échantillon de texte
def detect_separator(sample):
    sep_candidates = [',', ';', '\t']
    counts = {sep: sample.count(sep) for sep in sep_candidates}
    detected_sep = max(counts, key=counts.get)
    print(f"Séparateur détecté: '{detected_sep}' (compteurs: {counts})")
    return detected_sep

def preprocess_data(
    file_path: str = None,
    target_cols: list = None,
    test_size: float = 0.2,
    time_steps: int = 10,
    random_state: int = 42,
    save_scalers: bool = True,
    scalers_dir: str = None
):
    """
    Prétraite les données météo pour un modèle LSTM multivarié.
    """
    # Configuration des chemins
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if file_path is None:
        file_path = os.path.join(base_dir, '..', 'data', 'meteo_douala4.xlsx')
    file_path = os.path.abspath(file_path)
    
    if scalers_dir is None:
        scalers_dir = os.path.join(base_dir, '..', 'models', 'scalers')

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Fichier introuvable : {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    try:
        if ext in ['.xlsx', '.xls']:
            try:
                # Tentative de lecture en tant que vrai fichier Excel
                data = pd.read_excel(file_path)
            except Exception as e:
                print(f"⚠️ Le fichier avec extension {ext} ne semble pas être un vrai fichier Excel.")
                print(f"Erreur détectée : {e}")
                print("🔁 Tentative de lecture comme fichier CSV (renommé en .xlsx)...")
                # Lecture de l'échantillon pour détecter le séparateur
                with open(file_path, 'r', encoding='utf-8') as f:
                    sample = f.read(2048)
                sep = detect_separator(sample)
                data = pd.read_csv(file_path, sep=sep, encoding='utf-8', engine='python', on_bad_lines='skip')
        elif ext == '.csv':
            with open(file_path, 'r', encoding='utf-8') as f:
                sample = f.read(2048)
            sep = detect_separator(sample)
            data = pd.read_csv(file_path, sep=sep, encoding='utf-8', engine='python', on_bad_lines='skip')
        else:
            raise ValueError(f"❌ Format non supporté : {ext}")
    except UnicodeDecodeError as ue:
        print("Erreur d'encodage utf-8 détectée :", ue)
        print("🔁 Réessai avec l'encodage latin1...")
        with open(file_path, 'r', encoding='latin1') as f:
            sample = f.read(2048)
        sep = detect_separator(sample)
        data = pd.read_csv(file_path, sep=sep, encoding='latin1', engine='python', on_bad_lines='skip')
    except Exception as e:
        raise RuntimeError(f"Erreur lecture du fichier {file_path} : {e}")

    # Nettoyage des colonnes non numériques
    for col in list(data.columns):
        if pd.api.types.is_datetime64_any_dtype(data[col]) or data[col].dtype == object:
            try:
                data[col] = pd.to_numeric(data[col])
            except Exception:
                data.drop(columns=[col], inplace=True)

    # Renommage des colonnes
    rename_map = {
        'Température (°C)': 'Temperature',
        'Pression (hPa)': 'Pressure',
        'Humidité (%)': 'Humidity',
        'Vitesse du vent (m/s)': 'Wind',
        'Précipitation (mm)': 'Precipitation'
    }
    data.rename(columns=rename_map, inplace=True)

    # Sélection des colonnes cibles
    if target_cols is None:
        target_cols = [c for c in data.columns if 'temp' in c.lower() or 'precip' in c.lower()]
        print(f"Labels détectés pour target_cols: {target_cols}")
    for col in target_cols:
        if col not in data.columns:
            raise KeyError(f"Colonne cible manquante: {col}")

    # Sélection des features et targets, suppression des lignes avec valeurs manquantes
    feature_cols = [c for c in data.columns if c not in target_cols]
    df = data[feature_cols + target_cols].dropna(axis=0)

    # Normalisation
    scaler_X = MinMaxScaler()
    scaler_y = MinMaxScaler()
    X_scaled = scaler_X.fit_transform(df[feature_cols])
    y_scaled = scaler_y.fit_transform(df[target_cols])

    # Séparation train/test
    X_train_flat, X_test_flat, y_train_flat, y_test_flat = train_test_split(
        X_scaled, y_scaled,
        test_size=test_size,
        random_state=random_state
    )

    # Création des séquences temporelles
    def create_sequences(X, y, ts):
        Xs, ys = [], []
        for i in range(len(X) - ts):
            Xs.append(X[i:i+ts])
            ys.append(y[i+ts])
        return np.array(Xs), np.array(ys)

    X_train, y_train = create_sequences(X_train_flat, y_train_flat, time_steps)
    X_test, y_test = create_sequences(X_test_flat, y_test_flat, time_steps)

    # Mélange des données d'entraînement
    np.random.seed(random_state)
    perm = np.random.permutation(len(X_train))
    X_train = X_train[perm]
    y_train = y_train[perm]

    # Sauvegarde des scalers
    scalers = {'X': scaler_X, 'y': scaler_y}
    if save_scalers:
        os.makedirs(scalers_dir, exist_ok=True)
        joblib.dump(scaler_X, os.path.join(scalers_dir, 'scaler_X.pkl'))
        joblib.dump(scaler_y, os.path.join(scalers_dir, 'scaler_y.pkl'))

    return X_train, X_test, y_train, y_test, scalers

if __name__ == '__main__':
    X_train, X_test, y_train, y_test, scalers = preprocess_data()
    print(f"X_train shape: {X_train.shape}")
    print(f"y_train shape: {y_train.shape}")
    print(f"X_test shape: {X_test.shape}")
    print(f"y_test shape: {y_test.shape}")