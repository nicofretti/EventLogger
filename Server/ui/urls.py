from django.contrib import admin
from django.urls import path
import ui.views as views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('', views.homepage, name='homepage'),
    path('<int:pk>/', views.events, name='events'),
    path('<int:pk>/settings/', views.settings, name='settings'),
    path('<int:pk>/charts/', views.charts, name='charts'),
]