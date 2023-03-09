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

"""
1) User submits a form on the frontend --> React code should request /api/classify?{params}
2) Process params in here
3) Call the ML model (python code)
4) return a JSON response (serialize)
"""

# @api_view(['POST', 'DELETE'])
# @permission_classes((permissions.AllowAny,))
# def inference(request):
    # EITHER youtube link
    # OR file upload


    # song_name = request.GET.get("song_name", "")
    # song_artist = request.GET.get("song_artist", "")
    # song_album = request.GET.get("song_album", "")

    # if request.method == 'GET':
    #     try:
    #         song = Song.objects.get(song_name=song_name, song_artist=song_artist, song_album=song_album)
    #         serializer = SongSerializer(song, many=False)
    #         print(serializer.data)
    #         return Response(serializer.data)
    #     except:
    #         print(f"song with {song_name}, {song_artist}, {song_album} does not exist, inferencing...")

    #     song_data = _load_song(song_name, song_artist, song_album)

    #     if song_data is None: # song does not exist as an mp3
    #         return Response(_to_json(f"Song does not exist in database."), status= status.HTTP_400_BAD_REQUEST) # return json as error
        
    #     preprocessed_song = _preprocess_song(song_data)
    #     predicted_genre = _predict_song_genre(preprocessed_song)

    #     song = Song(song_name=song_name, song_artist=song_artist, song_album=song_album, song_genre=predicted_genre)
    #     song.save()
    #     serializer = SongSerializer(song, many=False)
    #     return Response(serializer.data)

    # elif request.method == "DELETE": # MUST BE PROTECTED
    #     try:
    #         song = Song.objects.get(song_name=song_name, song_genre=genre)
    #         song.delete()
    #         return Response(_to_json(f"Deleted song with {song_name}-{song_artist}-{song_album}"), status= status.HTTP_204_NO_CONTENT) # return json as error
    #     except:
    #         print(f"Song {song_name}-{song_artist}-{song_album} does not exist")
    #         return Response(_to_json(f"Song does not exist in database."), status= status.HTTP_400_BAD_REQUEST)


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
                    return Response(_to_json(f"{youtube_link} does not exist"))
        else:
            file_size = file.size
            file_name = file.name
            file_bin = file.read() # in bytes

            with open(f"{file_name}", "wb") as f: # FIXME: file saving????
                f.write(file_bin)

            genre = predict_genre(file_name)
            print(f"{file_name} - {convert_bytes(file_size)}")

            os.remove(file_name)

            return Response(_to_json(f"genre: {genre}"))
        
    return Response(_to_json(f"Saved {youtube_link}!"))
        

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def _list_songs(request):
    songlist = Song.objects.all()
    s = SongSerializer(songlist, many = True)
    return Response(s.data)
    

def _handle_youtube_link(yt_link):
    yt = YouTube(yt_link)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=".") # FIXME: ofile saving????
    base, ext = os.path.splitext(out_file)
    new_file_name = base + '.mp3'
    os.rename(out_file, new_file_name)
    return new_file_name


def _to_json(message):
    data = dict()
    data["detail"] = message
    return json.dumps(data)

def convert_bytes(size):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0
    return size