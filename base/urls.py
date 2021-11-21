from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginView, name="login"),
    path('logout/', views.logoutView, name="logout"),
    path('register/', views.registerView, name="register"),
    
    path('', views.home, name="home"),
    path('room/<str:roomID>/', views.room, name="room"),
    path('profile/<str:username>/', views.userProfile, name="profile"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:roomID>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:roomID>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:msgID>', views.deleteMessage, name="delete-message"),
    path('update-user/', views.updateUser, name="update-user"),
    
    path('topics/', views.topicView, name="topics"),
    path('activity/', views.activityView, name="activity"),
]
