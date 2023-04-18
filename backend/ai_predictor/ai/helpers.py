import io
from .model import predict
import numpy as np
import librosa
import math
import os
import sys


__all__ = ['predict_genre']

SR = 22050
N_MFCC = 13
# SIZE = (n_mfcc, TRACK_DURATION * SR / hop_length)

def predict_genre(model, file_path, model_no=1):
    if model_no == 1:
        mfccs = preprocess_audio_to_mfccs(file_path)
        # assert mfccs.shape == (1, 26, 65, 1) , f"Recieved {mfccs.shape}"
        genre = predict(model, mfccs=mfccs, model_no=model_no)
        print(genre)
        return genre
    elif model_no == 2:
        genre = predict(model, mfccs=None, model_no=model_no, file_path=file_path)
        return genre
    else:
        return None
    
def preprocess_audio_to_mfccs(file_path):
    frame_mfccs = get_frame_mfccs(file_path)
    print(f"Frame mfcc shape: {frame_mfccs.shape}")
    processed_data = np.array([reshape(i) for i in frame_mfccs]) 
    # processed_data = processed_data[np.newaxis, ...]
    print(f"Reshaped mfcc shape: {processed_data.shape}")
    return processed_data

def get_mfcc(path):
    track_duration = librosa.get_duration(path=path)
    hop_length = math.floor(track_duration*SR/130)
    # print(track_duration*SR/hop_length)
    # print(hop_length)
    audio, sr = librosa.load(path, sr=SR)
    mfccs = librosa.feature.mfcc(y=audio, sr=SR, n_mfcc=N_MFCC,hop_length=hop_length,n_fft=2048)
    return mfccs

def get_frame_mfccs(path):
    '''
    -------------------------------------------------
    Loads the .wav audio file and split into 3-second slices and then calculate mfccs for all slices
    -------------------------------------------------
    :params path : path to .wav file
    :returns : list of mfcc values'''
    audio, sr = librosa.load(path)
    frames = librosa.util.frame(audio, frame_length=sr*3, hop_length=sr*3)
    frame_mfccs = []
    for i in range(frames.shape[1]):
        mfccs = librosa.feature.mfcc(y=frames[:,i],sr=sr,n_mfcc=13,hop_length=512,n_fft=2048)
        frame_mfccs.append(mfccs)
    return np.array(frame_mfccs)
    

def reshape(data, shape=(26,65)):
    assert data.shape == (13,130) , f"The Data shape should be (13,130) but got {data.shape}"
    data = data.reshape(shape)
    data = np.expand_dims(data,axis=-1)
    return data

if __name__ == "__main__":
    predict_genre(sys.argv[1])