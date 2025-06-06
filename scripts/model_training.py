import os
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Input
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam
from data_preprocessing import preprocess_data
import pandas as pd


# 1. Configuration
#import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_PATH = os.path.join(BASE_DIR, 'data', 'meteo_douala4.xlsx')

print("Chemin absolu vers le fichier:", FILE_PATH)

MODEL_PATH = os.path.join('models', 'multivariate_meteo_lstm.keras')
TIME_STEPS = 10
EPOCHS = 50
BATCH_SIZE = 32

# 2. Prétraitement
X_train, X_test, y_train, y_test, scalers = preprocess_data(FILE_PATH, time_steps=TIME_STEPS)

# 3. Création du modèle
# 3. Création du modèle (version corrigée avec couche Input explicite)
model = Sequential([
    Input(shape=(X_train.shape[1], X_train.shape[2])),  # Définition claire de la forme des données en entrée
    LSTM(64, return_sequences=True),
    Dropout(0.2),
    LSTM(32),
    Dropout(0.2),
    Dense(y_train.shape[1])  # Sortie multivariée
])

# Compilation du modèle (optionnelle, mais recommandée pour lancer l'entraînement)
model.compile(optimizer=Adam(), loss='mse', metrics=['mae'])

# Affichage du résumé du modèle
model.summary()
 # Sortie multivariée

# 4. Compilation
model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')

# 5. Entraînement
early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
model.fit(X_train, y_train, 
          validation_data=(X_test, y_test),
          epochs=EPOCHS, 
          batch_size=BATCH_SIZE, 
          callbacks=[early_stop],
          verbose=1)
# 6. Sauvegarde du modèle
os.makedirs('models', exist_ok=True)
model.save(MODEL_PATH)

print(f"✅ Modèle entraîné et sauvegardé dans : {MODEL_PATH}")
