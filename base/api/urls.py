from django.urls import path
from . import views

# with prefix 'api/'
urlpatterns = [
    path('', views.getRoutes), # response how to use api
    path('rooms/', views.getRooms),
    path('room/<str:roomID>/', views.getRoom),
]