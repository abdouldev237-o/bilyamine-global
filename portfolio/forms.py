"""
Formulaires du portfolio.
"""

from django import forms
from django.core.validators import MinLengthValidator
from .models import Testimonial


class TestimonialForm(forms.ModelForm):
    """Formulaire de témoignage public."""
    name = forms.CharField(
        label="Nom complet",
        min_length=2,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Votre nom complet',
            'autocomplete': 'name'
        })
    )
    profession = forms.CharField(
        label="Profession",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Votre profession (facultatif)'
        })
    )
    company = forms.CharField(
        label="Entreprise",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Votre entreprise (facultatif)'
        })
    )
    message = forms.CharField(
        label="Votre témoignage",
        validators=[MinLengthValidator(15)],
        max_length=2000,
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'placeholder': 'Partagez votre expérience... (minimum 15 caractères)',
            'rows': 5
        })
    )
    rating = forms.IntegerField(
        label="Note",
        min_value=1,
        max_value=5,
        initial=5,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'min': 1,
            'max': 5
        })
    )
    project = forms.ModelChoiceField(
        label="Projet concerné",
        queryset=None,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Testimonial
        fields = ['name', 'profession', 'company', 'message', 'rating', 'project']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Project
        self.fields['project'].queryset = Project.objects.filter(is_published=True)
        self.fields['project'].empty_label = "— Sélectionner un projet —"

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.status = 'pending'
        instance.is_featured = False
        if commit:
            instance.save()
        return instance
