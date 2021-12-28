from django.contrib import admin
from django.urls import path
import ui.views as views

urlpatterns = [
    path('login/', views.login),
]