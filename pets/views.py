from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

# Create your views here.
from django.contrib import messages

from .models import Pet,PetType,Favorite
from django.http import JsonResponse
from .forms import PetForm
from ai_assistant.services import generate_pet_description


def home(request):
    featured_pets = Pet.objects.filter(
        status='available'
    ).select_related(
        'pet_type'
    ).order_by(
        '-created_at'
    )[:3]

    total_pets = Pet.objects.filter(
        status='available'
    ).count()

    context = {
        'featured_pets': featured_pets,
        'total_pets': total_pets,
    }

    return render(request, 'home.html', context)


def pet_list(request):
    pets = Pet.objects.select_related(
        'pet_type',
        'owner'
    ).order_by('-created_at')

    # Search by pet name, breed, or location
    search_query = request.GET.get('q', '').strip()

    if search_query:
        from django.db.models import Q

        pets = pets.filter(
            Q(name__icontains=search_query) |
            Q(breed__icontains=search_query) |
            Q(location__icontains=search_query)
        )

    # Filter by pet type
    pet_type_id = request.GET.get('pet_type', '').strip()

    if pet_type_id.isdigit():
        pets = pets.filter(pet_type_id=int(pet_type_id))

    # Filter by adoption status
    status = request.GET.get('status', '').strip()

    if status in ['available', 'reserved', 'adopted']:
        pets = pets.filter(status=status)

    pet_types = PetType.objects.order_by('name')

    return render(
        request,
        'pets/pet_list.html',
        {
            'pets': pets,
            'pet_types': pet_types,
            'search_query': search_query,
            'selected_pet_type': pet_type_id,
            'selected_status': status,
        }
    )

@login_required
@require_POST
def toggle_favorite(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id)

    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        pet=pet
    )

    if not created:
        favorite.delete()

    return redirect(request.POST.get('next') or 'home')

def pet_detail(request, pk):
    pet = get_object_or_404(
        Pet.objects.select_related('pet_type', 'owner'),
        pk=pk
    )

    is_favorite = False

    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(
            user=request.user,
            pet=pet
        ).exists()

    return render(
        request,
        'pets/pet_detail.html',
        {
            'pet': pet,
            'is_favorite': is_favorite,
        }
    )

@login_required
@require_POST
def generate_ai_description(request):
    name = request.POST.get('name', '').strip()
    pet_type_id = request.POST.get('pet_type', '').strip()
    breed = request.POST.get('breed', '').strip()
    age_years = request.POST.get('age_years', '0').strip()
    age_months = request.POST.get('age_months', '0').strip()
    location = request.POST.get('location', '').strip()
    personality = request.POST.get('personality', '').strip()

    if not name or not pet_type_id or not location:
        return JsonResponse({
            'error': 'Please enter the pet name, pet type, and location first.'
        }, status=400)

    try:
        pet_type = PetType.objects.get(pk=int(pet_type_id))

        age = f"{age_years} years and {age_months} months"

        description = generate_pet_description(
            name=name,
            pet_type=pet_type.name,
            breed=breed,
            age=age,
            location=location,
            personality=personality,
        )

        return JsonResponse({
            'description': description
        })

    except (ValueError, PetType.DoesNotExist):
        return JsonResponse({
            'error': 'Please select a valid pet type.'
        }, status=400)

    except Exception:
        return JsonResponse({
            'error': 'Unable to generate a description right now. Please try again.'
        }, status=500)    

@login_required
def add_pet(request):
    profile = getattr(request.user, 'profile', None)

    # Only pet owners and shelters can add pets
    if not profile or profile.user_type not in ['owner', 'shelter']:
        messages.error(
            request,
            'Only pet owners and animal shelters can add pets.'
        )
        return redirect('home')

    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)

        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()

            messages.success(
                request,
                f'{pet.name} has been added successfully!'
            )

            return redirect('pet_list')
    else:
        form = PetForm()

    return render(
        request,
        'pets/add_pet.html',
        {'form': form}
    )


@login_required
def edit_pet(request, pk):
    pet = get_object_or_404(
        Pet,
        pk=pk,
        owner=request.user
    )

    profile = getattr(request.user, 'profile', None)

    if not profile or profile.user_type not in ['owner', 'shelter']:
        messages.error(
            request,
            'You are not permitted to edit this listing.'
        )
        return redirect('pet_list')

    if request.method == 'POST':
        form = PetForm(
            request.POST,
            request.FILES,
            instance=pet
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                f'{pet.name} has been updated successfully!'
            )

            return redirect('pet_detail', pk=pet.pk)
    else:
        form = PetForm(instance=pet)

    return render(
        request,
        'pets/edit_pet.html',
        {
            'form': form,
            'pet': pet,
        }
    )


@login_required
def delete_pet(request, pk):
    pet = get_object_or_404(
        Pet,
        pk=pk,
        owner=request.user
    )

    if request.method == 'POST':
        pet_name = pet.name
        pet.delete()

        messages.success(
            request,
            f'{pet_name} has been deleted successfully.'
        )

        return redirect('pet_list')

    return render(
        request,
        'pets/delete_pet.html',
        {'pet': pet}
    )


@login_required
@require_POST
def toggle_favorite(request, pk):
    pet = get_object_or_404(Pet, pk=pk)

    favorite = Favorite.objects.filter(
        user=request.user,
        pet=pet
    )

    if favorite.exists():
        favorite.delete()
        messages.success(
            request,
            f'{pet.name} removed from your favorites.'
        )
    else:
        Favorite.objects.create(
            user=request.user,
            pet=pet
        )
        messages.success(
            request,
            f'{pet.name} added to your favorites.'
        )

    return redirect(request.POST.get('next') or 'pet_list')
