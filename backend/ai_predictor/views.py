from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from ai_predictor.models import Song
from ai_predictor.serializers import SongSerializer
from rest_framework import status
from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist
import pytube
from pytube import YouTube
import json
import os
from .ai.helpers import predict_genre
import audioread
import time
from moviepy.editor import *
from .ai.model import load_ai_model

"""
1) User submits a form on the frontend --> React code should request /api/classify?{params}
2) Process params in here
3) Call the ML model (python code)
4) return a JSON response (serialize)
"""

MODEL_NO = 1

def load_model():
    if MODEL_NO == 1:
        WEIGHTS_PATH =  f'{os.path.dirname(os.path.abspath(__file__))}/ai/models/cnn_model_2.h5'
        model = load_ai_model(WEIGHTS_PATH)
        return model
    elif MODEL_NO == 2:
        WEIGHTS_PATH =  f'{os.path.dirname(os.path.abspath(__file__))}/ai/models/model_weights.h5'
        MODEL_PATH =  f'{os.path.dirname(os.path.abspath(__file__))}/ai/models/model.json'
        model = load_ai_model(weights_path=WEIGHTS_PATH, model_json=MODEL_PATH)
        return model
    return None
    

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def classify(request):
    if request.method == "POST":
        file = request.FILES.get("file-upload", "")
        if (file == ""):
            if (request.POST.get("song-link-text") != ""):
                youtube_link = request.POST.get("song-link-text")
                try:
                    model = load_model()
                    new_file_name = _download_youtube_link_as_mp3_and_trim(youtube_link)
                    print(f"new file: {new_file_name}")
                    genre = predict_genre(model, new_file_name, model_no=MODEL_NO)
                    os.remove(new_file_name)
                    return Response(_to_json(f"genre: {genre}"))
                except (pytube.exceptions.VideoUnavailable, pytube.exceptions.RegexMatchError, KeyError) as e:
                    print("Error occured, video does not exist")
                    return Response(_to_json(f"Youtube link {youtube_link} does not exist or could not be downloaded due to copyright issues"))
                except (audioread.exceptions.NoBackendError) as er:
                    return Response(_to_json(f"{er}"))
        else:
            file_size = file.size
            file_name = file.name
            file_bin = file.read() # in bytes

            with open(f"{file_name}", "wb") as f: # FIXME: file saving????
                f.write(file_bin)

            try:
                model = load_model()
                genre = predict_genre(model, file_name, model_no=MODEL_NO)
                print(f"{file_name} - {convert_bytes(file_size)}")

                os.remove(file_name)

                return Response(_to_json(f"Genre is {genre}"))
            except (audioread.exceptions.NoBackendError) as er:
                    return Response(_to_json(f"{er}"))
        
    return Response(_to_json(f"Please provide a song input"))
        
def _download_youtube_link_as_mp3_and_trim(yt_link):
    yt = YouTube(yt_link)
    video = yt.streams.filter(only_audio=True).first()
    mp4_file = video.download(output_path=".") 

    base, ext = os.path.splitext(mp4_file)
    mp4_new_file = base+"_trimmed.mp4"
    trim_mp4_file(mp4_file, mp4_new_file)

    base, ext = os.path.splitext(mp4_new_file)
    video_path = mp4_new_file
    audio_path = base + ".mp3"
    MP4ToMP3(video_path, audio_path)

    os.remove(video_path)
    os.remove(mp4_file)
    return audio_path

def trim_mp4_file(in_file, out_file):
    START_TIME = "00:00:25"
    END_TIME = "00:02:00"
    command = f'ffmpeg -ss {START_TIME} -to {END_TIME} -i "{in_file}" -c copy "{out_file}"'
    os.system(command)

def MP4ToMP3(mp4, mp3):
    FILETOCONVERT = AudioFileClip(mp4)
    FILETOCONVERT.write_audiofile(mp3)
    FILETOCONVERT.close()

def _to_json(message):
    data_str ='{\"detail\": \"' + message + '\"}'
    print(data_str)
    return data_str

def convert_bytes(size):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0
    return size



# https://stackoverflow.com/questions/3844430/how-to-get-the-duration-of-a-video-in-python
# https://stackoverflow.com/questions/42438380/ffmpeg-in-python-script
# https://www.youtube.com/watch?v=SGsJc1K5xj8
# https://github.com/kkroening/ffmpeg-python

# https://www.youtube.com/watch?v=WeYsTmIzjkw reggae
# https://youtu.be/CICIOJqEb5c blues
# https://www.youtube.com/watch?v=dxkohu0iZPk hiphop
# own mp3 classical