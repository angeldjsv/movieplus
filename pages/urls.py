from django.urls import path
from . import views
from .views import (
                    HomePageView,
                    ContactanosPageView,
                    PeliculasPageView, 
                    ReviewsPageView, 
                    TopPageView,
                    LoginView, 
                    pelicula_detail,
                    editar_perfil,
                    my_profile
)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('contactanos/', ContactanosPageView.as_view(), name='contactanos'),
    path('peliculas/', PeliculasPageView.as_view(), name='peliculas'),
    path('reviews/', ReviewsPageView.as_view(), name='reviews'),
    path('top/', TopPageView.as_view(), name='top'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('peliculas/<int:pk>/', pelicula_detail, name='pelicula_detail'),
    path('peliculas/<int:pk>/review/', views.crear_review, name='crear_review'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('editar_perfil/', editar_perfil, name='editar_perfil'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
