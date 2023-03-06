from django.db import models

# Create your models here.

class Song(models.Model):
    song_name = models.CharField(max_length=100, default="") # either the song name from youtube link or mp3 file name
    song_genre = models.CharField(max_length=100, default="") # predicted song genre

    class Meta:
        ordering = ['song_genre']

    def __str__(self):
        return f"{self.song_name} - {self.song_genre}"