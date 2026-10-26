from django.urls import path
from . import views

urlpatterns = [
    path('', views.pet_list, name='pet_list'),
    path('add/', views.add_pet, name='add_pet'),

    path(
        'generate-ai-description/',
        views.generate_ai_description,
        name='generate_ai_description'
    ),

    path(
        'favorite/<int:pk>/',
        views.toggle_favorite,
        name='toggle_favorite'
    ),

    path('detail/<int:pk>/', views.pet_detail, name='pet_detail'),
    path('<int:pk>/edit/', views.edit_pet, name='pet_edit'),
    path('<int:pk>/delete/', views.delete_pet, name='pet_delete'),
]
