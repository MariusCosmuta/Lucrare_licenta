from django.db import models

# Create your models here.


class userlist(models.Model):
    anime_id = models.IntegerField()
    user_id = models.IntegerField()
    rating = models.BooleanField()

    def __str__(self):
        return str(self.anime_id) + '/' + str(self.user_id) + '/' + str(self.rating)
