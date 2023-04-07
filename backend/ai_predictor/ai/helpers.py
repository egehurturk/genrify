import io
from .model import predict

__all__ = ['predict_genre']

def predict_genre(file_path):
    predicted_genre = _model_predict(file_path)
    return predicted_genre

def _model_predict(song_path):
    """
    Use ML
    """
    genre = predict()
    return genre

