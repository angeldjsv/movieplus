from django.contrib import admin
from .models import Pelicula, Profile

admin.site.register(Pelicula)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'avatar']
    fields = ['user', 'avatar', 'bio']


# Register your models here.


