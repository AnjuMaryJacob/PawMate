from django.shortcuts import render

# Create your views here.
from .models import Service


def service_list(request):
    services = Service.objects.filter(
        is_active=True
    ).order_by('name')

    service_type = request.GET.get('type', '')
    city = request.GET.get('city', '').strip()

    if service_type:
        services = services.filter(
            service_type=service_type
        )

    if city:
        services = services.filter(
            city__icontains=city
        )

    context = {
        'services': services,
        'service_types': Service.SERVICE_TYPE_CHOICES,
    }

    return render(request, 'services/service_list.html', context)