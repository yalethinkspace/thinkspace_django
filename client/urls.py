from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/sign-up/', views.sign_up, name='sign-up'),
]
