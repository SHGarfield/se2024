from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.wechat_login, name='wechat_login'),
    path('upload_username/', views.upload_username, name='upload_username'),
]