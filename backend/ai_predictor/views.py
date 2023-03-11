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
                    new_file_name = _handle_youtube_link(youtube_link)
                    genre = predict_genre(new_file_name)
                    print(genre)
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
        
def _handle_youtube_link(yt_link):
    yt = YouTube(yt_link)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=".") 
    base, ext = os.path.splitext(out_file)
    new_file_name = base + '.mp3'
    os.rename(out_file, new_file_name)
    return new_file_name


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