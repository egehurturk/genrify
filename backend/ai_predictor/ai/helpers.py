import librosa
import soundfile as sf
import io

def handle_binary_song_data(bin_data):
    ios = io.BytesIO(bin_data)
    data, samplerate = sf.read(ios, channels=1, samplerate=44100, format="RAW", subtype="FLOAT")
    print(samplerate)
    print(data[0:10])

def _preprocess_song(song_data):
    return song_data

def _predict_song_genre(song_data):
    """
    Use ML
    """
    return "Rock"