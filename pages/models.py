from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

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
            MinValueValidator(1850),  # Primera película registrada
            MaxValueValidator(datetime.now().year)  # Año actual
        ]
    )
    director = models.CharField(max_length=100, default='Desconocido')
    genero = models.CharField(max_length=20, choices=GENEROS_CHOICES, default='otro')
    puntuacion = models.DecimalField(max_digits=2, decimal_places=1)

    def __str__(self):
        return self.titulo



# Create your models here.