from django.db import models

# Create your models here.


class anime_detail(models.Model):
    anime_id = models.IntegerField()
    title = models.CharField(max_length=50)
    title_english = models.CharField(max_length=50)
    title_synonyms = models.CharField(max_length=50)
    image_url = models.CharField(max_length=300)
    type = models.CharField(max_length=10)
    source = models.CharField(max_length=20)
    status = models.CharField(max_length=30)
    airing = models.BooleanField(default=False)
    aired = models.CharField(max_length=50)
    duration = models.CharField(max_length=30)
    score = models.FloatField()
    scored_by = models.IntegerField()
    rank = models.IntegerField()
    popularity = models.IntegerField()
    members = models.IntegerField()
    favorites = models.IntegerField()
    background = models.CharField(max_length=1000)
    premiered = models.CharField(max_length=15)
    producer = models.CharField(max_length=100)
    licensor = models.CharField(max_length=50)
    studio = models.CharField(max_length=30)
    genre = models.CharField(max_length=100)
    duration_min = models.FloatField()

    def __str__(self):
        return 'id:' + str(self.id) + ' anime_id: ' + str(self.anime_id) + ' title: ' + self.title
