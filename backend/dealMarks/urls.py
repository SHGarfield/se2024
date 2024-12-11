from django.urls import path
from . import views

urlpatterns = [
    path('addMarks/', views.addMarks, name='addMarks'),
    
]