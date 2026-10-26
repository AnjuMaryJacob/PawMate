from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class PetType(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.name


class Pet(models.Model):

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('unknown', 'Unknown'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('adopted', 'Adopted'),
    ]

    name = models.CharField(
        max_length=100
    )

    pet_type = models.ForeignKey(
        PetType,
        on_delete=models.PROTECT,
        related_name='pets'
    )

    breed = models.CharField(
        max_length=100,
        blank=True
    )

    age_years = models.PositiveIntegerField(
        default=0
    )

    age_months = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='unknown'
    )

    color = models.CharField(
        max_length=100,
        blank=True
    )

    description = models.TextField()

    location = models.CharField(
        max_length=200
    )

    vaccinated = models.BooleanField(
        default=False
    )

    medical_history = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to='pets/',
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='listed_pets'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.name} ({self.pet_type.name})"


class PetImage(models.Model):

    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(
        upload_to='pet_gallery/'
    )

    caption = models.CharField(
        max_length=200,
        blank=True
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Image of {self.pet.name}"


class Favorite(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_pets'
    )

    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'pet'],
                name='unique_user_favorite_pet'
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.pet.name}"