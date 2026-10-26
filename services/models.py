from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Service(models.Model):

    SERVICE_TYPE_CHOICES = [
        ('vet', 'Veterinary Hospital'),
        ('shelter', 'Pet Shelter'),
        ('boarding', 'Boarding Center'),
        ('grooming', 'Grooming Center'),
    ]

    name = models.CharField(
        max_length=200
    )

    service_type = models.CharField(
        max_length=20,
        choices=SERVICE_TYPE_CHOICES
    )

    description = models.TextField()

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=15
    )

    email = models.EmailField(
        blank=True
    )

    opening_hours = models.CharField(
        max_length=200,
        blank=True
    )

    image = models.ImageField(
        upload_to='services/',
        blank=True,
        null=True
    )

    website = models.URLField(
        blank=True
    )

    added_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='added_services'
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.name} - {self.get_service_type_display()}"