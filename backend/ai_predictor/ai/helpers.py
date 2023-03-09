import librosa
import soundfile as sf
import io
from .model import *

__all__ = ['predict_genre']

def predict_genre(file_path):
    data, sr = _load_file(file_path)
    preprocessed_data, sr = _preprocess_song(data, sr)
    predicted_genre = _model_predict(file_path)
    return predicted_genre

def _load_file(file_path):
    data, samplerate = librosa.load(file_path, sr=44100)
    assert samplerate == 44100
    return data, samplerate

def _preprocess_song(song_data, sr):
    return song_data, sr

def _model_predict(song_path):
    """
    Use ML
    """
    genre = predict(song_path)
    return genre

