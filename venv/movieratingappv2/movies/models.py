from django.db import models
from account.models import Account
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class MovieManager(models.Manager):
    def create_movie(self, name, year, rating):
        movie = self.create(name=name,year=year,rating=rating)
        # do something with the book
        return movie

class Movie(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    rating = models.FloatField()
    watched_by = models.ManyToManyField(Account)

    objects = MovieManager()

    class Meta:
        unique_together = (("name", "year"),)

    def __str__(self):
        return self.name + " (" + str(self.year) +")"