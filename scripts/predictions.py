import os
import numpy as np
import logging
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from data_preprocessing import preprocess_data
from sklearn.metrics import mean_absolute_error, mean_squared_error
from math import sqrt

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Définition des répertoires
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'models')
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
os.makedirs(MODELS_DIR, exist_ok=True)

def load_historical_data(file_path, target_cols):
    """Charge les données météo historiques pour comparaison avec les prévisions."""
    try:
        data = pd.read_excel(file_path, engine='openpyxl')  
        data.rename(columns={'Température (°C)': 'Temperature', 'Précipitation (mm)': 'Precipitation'}, inplace=True)
        historical_data = data[target_cols].tail(7)  
        logging.info("✅ Données historiques chargées pour validation.")
        return historical_data
    except Exception as e:
        logging.error("❌ Erreur lors du chargement des données historiques : %s", e)
        return None

def make_predictions(model_filename='multivariate_meteo_lstm.keras',
                     data_file=os.path.join(DATA_DIR, 'meteo_douala4.xlsx'),  
                     target_cols=['Temperature', 'Precipitation'],
                     horizon=7,
                     time_steps_options=[10, 15, 20]):  

    best_mae = float('inf')
    best_time_steps = None
    best_predictions = None

    for time_steps in time_steps_options:
        logging.info(f"\n🔄 Test avec time_steps = {time_steps}")

        try:
            model_path = os.path.join(MODELS_DIR, model_filename)
            model = load_model(model_path)
            logging.info("✅ Modèle chargé depuis %s", model_path)
        except Exception as e:
            logging.error("❌ Erreur de chargement du modèle : %s", e)
            raise

        try:
            X_train, X_test, y_train, y_test, scalers = preprocess_data(file_path=data_file, 
                                                                        target_cols=target_cols, 
                                                                        time_steps=time_steps)  
            logging.info("✅ Prétraitement des données effectué.")
        except Exception as e:
            logging.error("❌ Erreur lors du prétraitement des données : %s", e)
            raise

        try:
            last_seq = X_train[-1:].copy()
            num_features = last_seq.shape[2]
            num_targets = y_train.shape[1]
            non_target_size = num_features - num_targets

            raw_preds = []
            for _ in range(horizon):
                pred = model.predict(last_seq, verbose=0)[0]
                raw_preds.append(pred)

                exog = last_seq[:, -1:, :non_target_size]
                targ = pred.reshape(1, 1, num_targets)

                new_step = np.concatenate([exog, targ], axis=-1)
                last_seq = np.concatenate([last_seq[:, 1:, :], new_step], axis=1)

            preds_unscaled = scalers['y'].inverse_transform(np.array(raw_preds))

            if 'Precipitation' in target_cols:
                idx_precip = target_cols.index('Precipitation')
                preds_unscaled[:, idx_precip] = np.maximum(preds_unscaled[:, idx_precip], 0)

            for i in range(len(target_cols)):
                preds_unscaled[:, i] = [val if val < 100 else np.nan for val in preds_unscaled[:, i]]

            predictions_df = pd.DataFrame(preds_unscaled, columns=target_cols)
            logging.info("✅ Prédictions générées avec succès.")

            historical_data = load_historical_data(data_file, target_cols)
            if historical_data is not None:
                validation_df = pd.concat([historical_data.reset_index(drop=True), predictions_df], axis=1)
                validation_df.columns = ['Temp_Hist', 'Prec_Hist', 'Temp_Pred', 'Prec_Pred']
                print("\n📊 Comparaison des prévisions avec les données historiques :")
                print(validation_df)

                mae_temp = mean_absolute_error(validation_df['Temp_Hist'], validation_df['Temp_Pred'])
                rmse_temp = sqrt(mean_squared_error(validation_df['Temp_Hist'], validation_df['Temp_Pred']))
                logging.info(f"📉 MAE Température: {mae_temp:.4f}, RMSE Température: {rmse_temp:.4f}")

                if mae_temp < best_mae:
                    best_mae = mae_temp
                    best_time_steps = time_steps
                    best_predictions = predictions_df

            plot_predictions(validation_df)

        except Exception as e:
            logging.error("❌ Erreur lors de la génération des prévisions : %s", e)
            raise

    logging.info(f"🎯 Best time_steps: {best_time_steps} avec MAE = {best_mae:.4f}")
    return best_predictions

def plot_predictions(validation_df):
    """Affiche les prévisions sous forme de graphiques pour comparer avec les données historiques."""
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(validation_df.index, validation_df['Temp_Hist'], label="Température Historique", marker="o", linestyle="--")
    plt.plot(validation_df.index, validation_df['Temp_Pred'], label="Température Prédite", marker="o")
    plt.xlabel("Jour")
    plt.ylabel("Température (°C)")
    plt.title("Évolution de la Température")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(validation_df.index, validation_df['Prec_Hist'], label="Précipitation Historique", marker="o", linestyle="--")
    plt.plot(validation_df.index, validation_df['Prec_Pred'], label="Précipitation Prédite", marker="o")
    plt.xlabel("Jour")
    plt.ylabel("Précipitation (mm)")
    plt.title("Évolution des Précipitations")
    plt.legend()

    plt.tight_layout()
    plt.show()
    logging.info("✅ Visualisation des prévisions affichée avec succès.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Générer des prévisions météorologiques avec un modèle LSTM.")
    args = parser.parse_args()

    predictions_df = make_predictions()