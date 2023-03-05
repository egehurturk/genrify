from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from ai_predictor.models import Song
from ai_predictor.serializers import SongSerializer
from rest_framework import status
from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist
import json

"""
1) User submits a form on the frontend --> React code should request /api/classify?{params}
2) Process params in here
3) Call the ML model (python code)
4) return a JSON response (serialize)

Note: the ML inference should not be blocking but should update later (ajax or async)
"""


@api_view(['GET', 'DELETE'])
@permission_classes((permissions.AllowAny,))
def inference(request):
    song_name = request.GET.get("song_name", "")
    song_artist = request.GET.get("song_artist", "")
    song_album = request.GET.get("song_album", "")

    if request.method == 'GET':
        try:
            song = Song.objects.get(song_name=song_name, song_artist=song_artist, song_album=song_album)
            serializer = SongSerializer(song, many=False)
            print(serializer.data)
            return Response(serializer.data)
        except:
            print(f"song with {song_name}, {song_artist}, {song_album} does not exist, inferencing...")

        song_data = _load_song(song_name, song_artist, song_album)

        if song_data is None: # song does not exist as an mp3
            return Response(_to_json(f"Song does not exist in database."), status= status.HTTP_400_BAD_REQUEST) # return json as error
        
        preprocessed_song = _preprocess_song(song_data)
        predicted_genre = _predict_song_genre(preprocessed_song)

        song = Song(song_name=song_name, song_artist=song_artist, song_album=song_album, song_genre=predicted_genre)
        song.save()
        serializer = SongSerializer(song, many=False)
        return Response(serializer.data)

    elif request.method == "DELETE": # MUST BE PROTECTED
        try:
            song = Song.objects.get(song_name=song_name, song_artist=song_artist, song_album=song_album)
            song.delete()
            return Response(_to_json(f"Deleted song with {song_name}-{song_artist}-{song_album}"), status= status.HTTP_204_NO_CONTENT) # return json as error
        except:
            print(f"Song {song_name}-{song_artist}-{song_album} does not exist")
            return Response(_to_json(f"Song does not exist in database."), status= status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def _list_songs(request):
    songlist = Song.objects.all()
    s = SongSerializer(songlist, many = True)
    return Response(s.data)
    
def _preprocess_song(song_data):
    return song_data

def _to_json(message):
    data = dict()
    data["detail"] = message
    return json.dumps(data)

def _load_song(song_name, song_artist, song_album):
    """
    Check if the song with given values exists, if exists return the wav file, else return None
    """
    return None

def _predict_song_genre(song_data):
    """
    Use ML
    """
    return "Rock"