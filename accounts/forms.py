from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class RegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    user_type = forms.ChoiceField(
        choices=Profile.USER_TYPE_CHOICES,
        initial='adopter',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number'
        })
    )

    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your city'
        })
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'user_type',
            'phone',
            'city',
            'password1',
            'password2',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            profile, created = Profile.objects.get_or_create(
                user=user
            )
            profile.user_type = self.cleaned_data['user_type']
            profile.phone = self.cleaned_data['phone']
            profile.city = self.cleaned_data['city']
            profile.save()

        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'user_type',
            'phone',
            'address',
            'city',
            'profile_image',
        ]

        widgets = {
            'user_type': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your phone number',
                }
            ),
            'address': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your address',
                    'rows': 3,
                }
            ),
            'city': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your city',
                }
            ),
        }

