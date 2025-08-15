from django import forms
from .models import Profile, Review

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comentario', 'rating']
        widgets = {
            'comentario': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-light border border-secondary rounded-3',
                'placeholder': 'Escribe tu opinión sobre la película...',
                'rows': 4,
                'style': 'resize:none; font-size:15px;'
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select bg-dark text-light border border-secondary rounded-3',
                'style': 'font-size:15px;'
            }, choices=[(x / 2, f"{x / 2} ⭐") for x in range(1, 11)])
        }





