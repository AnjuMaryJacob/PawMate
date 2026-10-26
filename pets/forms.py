from django import forms
from .models import Pet


class PetForm(forms.ModelForm):

    class Meta:
        model = Pet

        fields = [
            'name',
            'pet_type',
            'breed',
            'age_years',
            'age_months',
            'gender',
            'color',
            'description',
            'location',
            'vaccinated',
            'medical_history',
            'image',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter pet name'
            }),

            'pet_type': forms.Select(attrs={
                'class': 'form-control'
            }),

            'breed': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter breed'
            }),

            'age_years': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),

            'age_months': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '11'
            }),

            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),

            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter pet color'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe the pet and its personality',
                'rows': 4
            }),

            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter city or location'
            }),

            'vaccinated': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),

            'medical_history': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter medical history, if any',
                'rows': 3
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }
