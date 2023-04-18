import sys
import numpy as np
import librosa
import tensorflow as tf
from keras.models import model_from_json
import os

__all__ = ["predict"]

def load_ai_model(weights_path, model_json=None):
    if model_json is None:
          model = tf.keras.models.load_model(f'{os.path.dirname(os.path.abspath(__file__))}/models/cnn_model_2.h5')
          return model
     
    with open(model_json, "r") as model_file:
        trained_model = model_from_json(model_file.read())
        
    trained_model.load_weights(weights_path)
    trained_model.compile(
        loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"]
    )
    return trained_model
          
def extract_audio_features(file):
    "Extract audio features from an audio file for genre classification"
    timeseries_length = 128
    features = np.zeros((1, timeseries_length, 33), dtype=np.float64)

    y, sr = librosa.load(file)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=512, n_mfcc=13)
    spectral_center = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=512)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr, hop_length=512)
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr, hop_length=512)

    features[0, :, 0:13] = mfcc.T[0:timeseries_length, :]
    features[0, :, 13:14] = spectral_center.T[0:timeseries_length, :]
    features[0, :, 14:26] = chroma.T[0:timeseries_length, :]
    features[0, :, 26:33] = spectral_contrast.T[0:timeseries_length, :]
    return features

def get_genre(modela, music_path):
    genre_list = [
        "classical",
        "country",
        "disco",
        "hiphop",
        "jazz",
        "metal",
        "pop",
        "reggae",
    ]

    "Predict genre of music using a trained model"
    prediction = modela(extract_audio_features(music_path))
    predict_genre = genre_list[np.argmax(prediction)]
    return predict_genre

GENRES = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']

def predict(model, mfccs=None, model_no=1, file_path = None):
    if model is None:
         return None
    if model_no == 1 and mfccs is not None:
        pred = model(mfccs)
        print(f"pred after modal predict mfcc shape: {pred.shape}")
        preds = []
        for i in pred:
                out = np.argmax(i)
                preds.append(out)
        pred_g = GENRES[preds[0]]
        return pred_g
    elif model_no == 2 and file_path is not None:
        pred_g = get_genre(model, file_path)
        return pred_g
         
    



