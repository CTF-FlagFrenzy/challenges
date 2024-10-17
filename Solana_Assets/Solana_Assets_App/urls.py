from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('news/', views.news, name='news'),
    path('login/', views.login_view, name='login'),
]