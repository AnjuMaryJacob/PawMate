from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import RegistrationForm
from .forms import ProfileUpdateForm

def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


@login_required
def profile(request):
    # Get the user's profile, or create one if it doesn't exist
    profile_obj, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile_obj,
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Your profile was updated successfully!'
            )
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile_obj)

    return render(
        request,
        'accounts/profile.html',
        {
            'profile': profile_obj,
            'form': form,
        }
    )
