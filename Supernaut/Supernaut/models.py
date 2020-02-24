from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

    def get_absolute_url(self):
        return f'/artist/{self}/'


class Album(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    year = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Track(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    index = models.IntegerField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='tracks')
    duration = models.CharField(max_length=255, db_index=False, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('index',)
