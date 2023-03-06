from django.contrib.auth.models import User, Group
from rest_framework import serializers
from ai_predictor.models import Song

class SongSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = ['id', 'song_name', 'song_genre']
