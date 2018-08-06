from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/sign-up/', views.sign_up, name='sign-up'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'), 
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/change_password/', views.change_password, name='change_password'),
    path('dashboard/basic_info/', views.dashboard_basic_info, name='basic_info'),
]
 
