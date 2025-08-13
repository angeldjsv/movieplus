from django.urls import path
from . import views
from .views import LoginView
from .views import HomePageView, AboutPageView, PeliculasPageView, ForoPageView, TopPageView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('peliculas/', PeliculasPageView.as_view(), name='peliculas'),
    path('foro/', ForoPageView.as_view(), name='foro'),
    path('top/', TopPageView.as_view(), name='top'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
