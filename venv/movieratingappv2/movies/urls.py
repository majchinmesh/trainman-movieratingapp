
from django.urls import path,include
from movies import views
from rest_framework import routers




router = routers.DefaultRouter()
router.register('',views.MovieView)

urlpatterns = [
    #path('', views.movieList.as_view()),
    path('',include(router.urls)),
]