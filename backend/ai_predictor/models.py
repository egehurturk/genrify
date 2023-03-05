from django.db import models

# Create your models here.

class Song(models.Model):
    song_name = models.CharField(max_length=100, default="")
    song_artist = models.CharField(max_length=100, default="")
    song_album = models.CharField(max_length=100, default="")
    song_genre = models.CharField(max_length=100, default="")

    class Meta:
        ordering = ['song_genre']

    def __str__(self):
        return f"{self.song_name} - {self.song_artist} - {self.song_album}"