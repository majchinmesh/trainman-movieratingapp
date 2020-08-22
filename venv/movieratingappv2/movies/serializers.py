from rest_framework import serializers
from . models import Movie
from account.models import Account

class accountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("id","username")

class MovieSerializer(serializers.ModelSerializer):
    #watched_by = accountSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ("id","name","year","rating")