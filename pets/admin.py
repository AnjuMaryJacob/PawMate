from django.contrib import admin

# Register your models here.
from .models import PetType, Pet, PetImage, Favorite

admin.site.register(PetType)
admin.site.register(Pet)
admin.site.register(PetImage)
admin.site.register(Favorite)