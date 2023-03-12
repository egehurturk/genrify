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

"""
1) User submits a form on the frontend --> React code should request /api/classify?{params}
2) Process params in here
3) Call the ML model (python code)
4) return a JSON response (serialize)
"""

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def classify(request):
    if request.method == "POST":
        file = request.FILES.get("file-upload", "")
        if (file == ""):
            if (request.POST.get("song-link-text") != ""):
                youtube_link = request.POST.get("song-link-text")
                try:
                    new_file_name = _download_youtube_link_as_mp3_and_trim(youtube_link)
                    print(f"new file: {new_file_name}")
                    genre = predict_genre(new_file_name)
                    os.remove(new_file_name)
                    return Response(_to_json(f"genre: {genre}"))

                except (pytube.exceptions.VideoUnavailable, pytube.exceptions.RegexMatchError) as e:
                    print("Error occured, video does not exist")
                    print(e)
                    return Response(_to_json(f"Youtube link {youtube_link} does not exist"))
                except (audioread.exceptions.NoBackendError) as er:
                    return Response(_to_json(f"{er}"))
        else:
            file_size = file.size
            file_name = file.name
            file_bin = file.read() # in bytes

            with open(f"{file_name}", "wb") as f: # FIXME: file saving????
                f.write(file_bin)

            try:
                genre = predict_genre(file_name)
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
    END_TIME = "00:01:25"
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


# FIXME: convert system call to ffmpeg-python, in trim_video check for in file duration to be bigger than 1