from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Pelicula
from django.core.paginator import Paginator


# Create your views here.
class HomePageView(TemplateView):
    template_name = "home.html"

class AboutPageView(TemplateView):
    template_name = "about.html"

class PeliculasPageView(TemplateView):
    template_name = "peliculas.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        genero = self.request.GET.get('genero')
        decada = self.request.GET.get('decada')
        orden = self.request.GET.get('orden')

        peliculas = Pelicula.objects.all()

        if genero:
            peliculas = peliculas.filter(genero=genero)

        if decada:
            try:
                inicio = int(decada)
                fin = inicio + 9
                peliculas = peliculas.filter(anio_lanzamiento__range=(inicio, fin))
            except ValueError:
                pass

        # 🔄 Aplicar ordenamiento
        if orden == "fecha_asc":
            peliculas = peliculas.order_by('anio_lanzamiento')
        elif orden == "fecha_desc":
            peliculas = peliculas.order_by('-anio_lanzamiento')
        elif orden == "titulo_desc":
            peliculas = peliculas.order_by('-titulo')
        else:
            # Por defecto: título ascendente
            peliculas = peliculas.order_by('titulo')

        # Paginación
        paginator = Paginator(peliculas, 20)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        return context


class ForoPageView(TemplateView):
    template_name = "foro.html"

class TopPageView(TemplateView):
    template_name = "top.html"
