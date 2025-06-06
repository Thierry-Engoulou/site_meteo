import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

SEQUENCE_LENGTH = 16
FEATURE_DIM = 4  # Temperature, Pression, Humidite, Vent


def construire_modele():
    model = Sequential([
        LSTM(64, input_shape=(SEQUENCE_LENGTH, FEATURE_DIM)),
        Dense(FEATURE_DIM)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model


def entrainer(X, y):
    model = construire_modele()
    model.fit(X, y, epochs=50, batch_size=32)
    model.save(os.path.join(os.path.dirname(__file__), "..", "data", "modele_lstm.h5"))