from django.db import models
from django.db.models import Model, Avg
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
from math import floor

class Pelicula(models.Model):
    GENEROS_CHOICES = [
        ('accion', 'Acción'),
        ('animacion', 'Animación'),
        ('aventura', 'Aventura'),
        ('biografia', 'Biografía'),
        ('ciencia_ficcion', 'Ciencia Ficción'),
        ('comedia', 'Comedia'),
        ('crimen', 'Crimen'),
        ('deporte', 'Deporte'),
        ('documental', 'Documental'),
        ('drama', 'Drama'),
        ('fantasia', 'Fantasía'),
        ('guerra', 'Guerra'),
        ('historia', 'Historia'),
        ('misterio', 'Misterio'),
        ('musical', 'Musical'),
        ('romance', 'Romance'),
        ('superheroes', 'Superhéroes'),
        ('suspenso', 'Suspenso'),
        ('terror', 'Terror'),
        ('thriller', 'Thriller'),
        ('western', 'Western'),

        # Aca podemos seguir añadiendo géneros

        ('otro', 'Otro'),
    ]

    titulo = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='peliculas/', blank=True, null=True)
    descripcion = models.TextField()
    anio_lanzamiento = models.IntegerField(
        default=2000,
        validators=[
            MinValueValidator(1850),
            MaxValueValidator(datetime.now().year)
        ]
    )
    director = models.CharField(max_length=100, default='Desconocido')
    genero = models.CharField(max_length=20, choices=GENEROS_CHOICES, default='otro')
    puntuacion = models.DecimalField(
        max_digits=3, 
        decimal_places=1,
        validators=[MinValueValidator(0.5), MaxValueValidator(5.0)],
        default=3.0,
    )

    def __str__(self):
        return self.titulo

    @property
    def promedio_rating(self):
        promedio = self.reviews.aggregate(promedio=Avg('rating'))['promedio']
        return round(promedio, 1) if promedio is not None else 0
    
    @property
    def estrellas_completas(self):
        return floor(self.promedio_rating)

    @property
    def media_estrella(self):
        resto = self.promedio_rating - self.estrellas_completas
        return 1 if 0.25 <= resto < 0.75 else 0

    @property
    def estrellas_vacias(self):
        return 5 - self.estrellas_completas - self.media_estrella
    
    @property
    def total_reviews(self):
        return self.reviews.count()


User = get_user_model()
    
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg', blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"

class Review(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.DecimalField(
        max_digits=2, 
        decimal_places=1,
        validators=[MinValueValidator(0.5), MaxValueValidator(5.0)]
    )
    comentario = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review de {self.user.username} sobre {self.pelicula.titulo} - Rating: ⭐{self.rating}"

# Create your models here.
