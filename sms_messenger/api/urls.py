from django.urls import path

from . import views


urlpatterns = [
    path('v1/messages', views.messages, name='messages'),
]
