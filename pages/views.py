from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, CreateView
from .forms import ProfileForm, RegistroForm
from .models import Pelicula, Review, Profile
from math import floor
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView
from django.db.models import Avg, Count
from django.urls import reverse_lazy
from datetime import datetime


# Create your views here.
class HomePageView(TemplateView):
    template_name = "home.html"

class AcercaPageView(TemplateView):
    template_name = "acerca.html"

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
        paginator = Paginator(peliculas, 15) # 15 películas por página
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        return context


class ReviewsPageView(TemplateView):
    template_name = "reviews.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reseñas'] = Review.objects.all().order_by('-fecha_creacion')
        return context


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comentario']

def calcular_estrellas(valor):
    completas = int(valor)
    resto = valor - completas
    media = 1 if 0.25 <= resto < 0.75 else 0
    vacías = 5 - completas - media
    return completas, media, vacías

@login_required

def pelicula_detail(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)

    # Obtener reseñas como lista para poder modificarlas
    reviews = list(pelicula.reviews.select_related('user__profile'))

    # Calcular estrellas por reseña individual
    for r in reviews:
        r.estrellas_completas, r.media_estrella, r.estrellas_vacias = calcular_estrellas(r.rating)

    # Obtener reseña del usuario actual (si existe)
    user_review = Review.objects.filter(pelicula=pelicula, user=request.user).first()

    # Calcular estrellas para el promedio general
    promedio = pelicula.promedio_rating or 0
    estrellas_completas, media_estrella, estrellas_vacias = calcular_estrellas(promedio)

    # Procesar formulario de reseña
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=user_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.pelicula = pelicula
            review.user = request.user
            review.save()
            return redirect('pelicula_detail', pk=pelicula.pk)
    else:
        form = ReviewForm(instance=user_review)

    return render(request, 'pelicula_detail.html', {
        'pelicula': pelicula,
        'reseñas': reviews,  # 👈 Este es el que debes usar en el template
        'form': form,
        'estrellas_completas': estrellas_completas,
        'media_estrella': media_estrella,
        'estrellas_vacias': estrellas_vacias,
    })




@login_required
def crear_review(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.pelicula = pelicula
            review.user = request.user
            review.save()
            return redirect('pelicula_detail', pk=pelicula.pk)
    else:
        form = ReviewForm()

    return render(request, 'crear_review.html', {
        'form': form,
        'pelicula': pelicula
    })

@login_required
def my_profile(request):
    perfil, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'my_profile.html', {'perfil': perfil})

@login_required
def editar_perfil(request):
    # Verifica si el perfil existe, si no lo crea
    perfil, creado = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('editar_perfil')
    else:
        form = ProfileForm(instance=perfil)

    return render(request, 'editar_perfil.html', {'form': form})


class TopPageView(TemplateView):
    template_name = "top.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        año_actual = datetime.now().year

        # Top del año
        top_del_año = (
            Review.objects
            .filter(fecha_creacion__year=año_actual)
            .values('pelicula__id', 'pelicula__titulo', 'pelicula__anio_lanzamiento')
            .annotate(promedio=Avg('rating'), total=Count('id'))
            .order_by('-promedio')[:10]
        )

        # Top general
        top_general = (
            Review.objects
            .values('pelicula__id', 'pelicula__titulo', 'pelicula__anio_lanzamiento')
            .annotate(promedio=Avg('rating'), total=Count('id'))
            .order_by('-promedio')[:10]
        )

        context['top_del_año'] = top_del_año
        context['top_general'] = top_general
        context['año_actual'] = año_actual
        return context


class SignupView(FormView):
    template_name = "signup.html"
    form_class = RegistroForm  # usa el formulario traducido
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    
class LoginView(DjangoLoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


