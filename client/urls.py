from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/sign_up/', views.sign_up, name='sign_up'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'), 
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/profile/', views.dashboard_profile, name='dashboard_profile'),
    path('dashboard/change_password/', views.change_password, name='change_password'),
]
 
