from django.urls import path
import api.views as views

urlpatterns = [
    path('logger', views.log, name='api_logger'),
]