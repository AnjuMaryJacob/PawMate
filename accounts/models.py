from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Profile(models.Model):

    USER_TYPE_CHOICES = [
        ('adopter', 'Adopter'),
        ('owner', 'Pet Owner'),
        ('shelter', 'Animal Shelter'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='adopter'
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"