from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models import Q

from pets.models import Pet


class AdoptionApplication(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]

    pet = models.ForeignKey(
        Pet,
        on_delete=models.PROTECT,
        related_name='adoption_applications'
    )

    applicant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='adoption_applications'
    )

    reason = models.TextField()

    experience = models.TextField(
        blank=True
    )

    living_environment = models.TextField()

    phone = models.CharField(
        max_length=15
    )

    address = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['pet', 'applicant'],
                condition=Q(status='pending'),
                name='unique_pending_pet_application'
            )
        ]

    def __str__(self):
        return (
            f"{self.applicant.username} - "
            f"{self.pet.name} - {self.status}"
        )