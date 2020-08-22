from django.shortcuts import render
from . models import Movie
from rest_framework import status
from . serializers import MovieSerializer
from . scraper import Scraper
from account.models import Account
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.core.validators import URLValidator
from django.core.validators import ValidationError
from django.db import IntegrityError


class MovieView(viewsets.ModelViewSet):
    WATCHED_BY = "watched_by"
    IMDB_URL = "imdb_url"

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        instance = self.get_object()
        token = Token.objects.get(key=request.auth)
        if self.WATCHED_BY in request.data and request.data[self.WATCHED_BY]: # just need a boolean true WATCHED_BY in the patch request
            try:
                user = Account.objects.get(pk=token.user_id)
                instance.watched_by.add(user)
                instance.save()
            except :
                pass
            request.data.pop(self.WATCHED_BY)
        return self.update(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if(self.WATCHED_BY in request.query_params):
            print(self.WATCHED_BY)
            queryset = self.filter_queryset(Movie.objects.filter(watched_by__id=1))
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    
    def create(self, request, *args, **kwargs):
        print(request.data)
        if self.IMDB_URL in request.data: # just need a boolean true WATCHED_BY in the patch request
            url = request.data[self.IMDB_URL]
            validate = URLValidator()
            try:
                validate(url)
                imdb_scraper = Scraper(url)
                movies = imdb_scraper.getMovies()
                update_count = 0
                insert_count = 0 
                for mo in movies:
                    try:
                        movie, created = Movie.objects.update_or_create(
                            name=mo["name"], year=mo["year"], defaults={"rating": mo["rating"]})
                        if created :
                            insert_count+=1
                        else :
                            update_count+=1
                    except:
                        pass
            except ValidationError as exception:
                return Response({"reason":"Invalid URL"},status=status.HTTP_400_BAD_REQUEST)
            except Exception as ex:
                print(ex)
                return Response({"reason":"Error while parsing URL"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({"data":{
                    "status": "Uploaded movies from url",
                    "updated" : update_count,
                    "inserted":insert_count
                    }
                },status=status.HTTP_201_CREATED)
        serializer = self.get_serializer(data=request.data)
        valid = serializer.is_valid(raise_exception=False)
        print(serializer.errors)
        #self.perform_create(serializer)
        if(valid or "non_field_errors" in serializer.errors ):
            movie, created = Movie.objects.update_or_create(name=request.data["name"], year=request.data["year"], defaults={"rating": request.data["rating"]})
            headers = self.get_success_headers(serializer.data)
            if(created):
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)