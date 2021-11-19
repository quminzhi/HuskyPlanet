from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message
from .forms import RoomForm

# Create your views here.

def loginView(request):
    page = 'login'
    
    if (request.user.is_authenticated):
        return redirect('home')
    
    if (request.method == 'POST'):
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        # check if user exists
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")
        # authenticate
        user = authenticate(request, username=username, password=password)
        if (user is not None):
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password incorrect")
    
    context = {
        'page': page,
    }
    
    return render(request, 'base/login_register.html', context)

def logoutView(request):
    logout(request)
    return redirect('home')

def registerView(request):
    page = 'register'
    form = UserCreationForm()
    
    if (request.method == 'POST'):
        form = UserCreationForm(request.POST)
        if (form.is_valid()):
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
            
    context = {
        'page': page,
        'form': form,
    }
    
    return render(request, 'base/login_register.html', context)

def home(request):
    if request.GET.get('q') != None:
        q = request.GET.get('q')
    else:
        q = ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)
    )
    # rooms = Room.objects.filter(topic__name__contains=q)
    # rooms = Room.objects.filter(topic__name__startswith=q)
    topics = Topic.objects.all()
    roomCnt = rooms.count()
    
    context = {
        'rooms': rooms,
        'topics': topics,
        'roomCnt': roomCnt,
    }
    
    # implicit directory basename is base/templates/ in default in Django
    return render(request, 'base/home.html', context) 

def room(request, roomID):
    room = Room.objects.get(id=roomID)
    room_messages = Message.objects.filter(room__name=room).order_by('-created')
    participants = room.participants.all()

    if (request.method == 'POST'):
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', roomID=room.id)
    
    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants,
    }

    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    
    # for post request
    if (request.method == 'POST'):
        form = RoomForm(request.POST)
        if (form.is_valid()):
            form.save()
            return redirect('home')
    
    context = {
        'form': form,
    }
    
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, roomID):
    room = Room.objects.get(id=roomID)
    form = RoomForm(instance=room) # prefill form with room
    
    if (request.method == 'POST'):
        form = RoomForm(request.POST, instance=room) # POST data will replace room data
        if (form.is_valid()):
            form.save()
            return redirect('home')
        
    context = {
        'form': form,
    }
    
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, roomID):
    room = Room.objects.get(id=roomID)
    if (request.method == 'POST'):
        room.delete()
        return redirect('home')

    context = {
        'obj': room,
    }
    
    return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def deleteMessage(request, msgID):
    message = Message.objects.get(id=msgID)
    
    if (request.user != message.user):
        return HttpResponse('No permission')
    
    if (request.method == 'POST'):
        message.delete()
        return redirect('home')

    context = {
        'obj': message,
    }
    
    return render(request, 'base/delete.html', context)