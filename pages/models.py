from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

class Pelicula(models.Model):
    GENEROS_CHOICES = [
        ('accion', 'Acción'),
        ('drama', 'Drama'),
        ('comedia', 'Comedia'),
        ('terror', 'Terror'),
        ('romance', 'Romance'),
        ('documental', 'Documental'),
        ('animacion', 'Animación'),
        ('ciencia_ficcion', 'Ciencia Ficción'),
        ('fantasia', 'Fantasía'),
        ('aventura', 'Aventura'),
        ('musical', 'Musical'),
        ('biografia', 'Biografía'),
        ('historia', 'Historia'),
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