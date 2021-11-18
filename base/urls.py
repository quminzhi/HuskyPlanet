from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('room/<str:roomID>/', views.room, name="room"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:roomID>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:roomID>/', views.deleteRoom, name="delete-room"),
]
