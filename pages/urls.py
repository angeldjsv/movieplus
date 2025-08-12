from django.urls import path
from .views import (
    HomePageView,
    AboutPageView,
    PeliculasPageView,
    ForoPageView,
    TopPageView
)
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('peliculas/', PeliculasPageView.as_view(), name='peliculas'),
    path('foro/', ForoPageView.as_view(), name='foro'),
    path('top/', TopPageView.as_view(), name='top'),
]