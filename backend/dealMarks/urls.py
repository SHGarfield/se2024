from django.urls import path
from . import views

urlpatterns = [
    path('addMarks/', views.addMarks, name='addMarks'),
    path('getMarks/', views.getMarks, name='getMarks'),
    path('getAllMarks/', views.getAllMarks, name='getAllMarks'),
    path('setRouteIsPrivate/', views.setRouteIsPrivate, name='setRouteIsPrivate'),
    path('deleteRoute/', views.deleteRoute, name='deleteRoute'),
    path('modifyMarks/', views.modifyMarks, name='modifyMarks'),
]