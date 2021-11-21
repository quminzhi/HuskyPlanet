from django.contrib import auth
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm

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
        Q(topic__name__icontains=q)
        # | Q(name__icontains=q) # bit operation
    )
    # rooms = Room.objects.filter(topic__name__contains=q)
    # rooms = Room.objects.filter(topic__name__startswith=q)
    topics = Topic.objects.all()
    topics_display = topics[0:5]
    roomCnt = rooms.count()
    room_messages = Message.objects.all().filter(
        Q(room__topic__name__icontains=q)
    )

    context = {
        'rooms': rooms,
        'topics': topics,
        'topics_display': topics_display,
        'roomCnt': roomCnt,
        'room_messages': room_messages,
    }
    
    # implicit directory basename is base/templates/ in default in Django
    return render(request, 'base/home.html', context) 

def room(request, roomID):
    room = Room.objects.get(id=roomID)
    room_messages = Message.objects.filter(room__name=room)
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

def userProfile(request, username):
    user = User.objects.get(username=username)
    rooms = Room.objects.filter(host=user.id)
    room_messages = Message.objects.filter(user=user.id)
    topics = Topic.objects.all()
    topics_display = topics[0:5]
    
    context = {
        'user': user,
        'rooms': rooms,
        'room_messages': room_messages,
        'topics': topics,
        'topics_display': topics_display,
    }
    
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    # for post request
    if (request.method == 'POST'):
        # create topic in database if it doesn't exist
        topic_name = request.POST.get('room_topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        # update database for customized form
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('room_name'),
            description=request.POST.get('description')
        )
        return redirect('home')
    
    context = {
        'form': form,
        'topics': topics,
    }
    
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, roomID):
    room = Room.objects.get(id=roomID)
    form = RoomForm(instance=room) # prefill form with room
    topics = Topic.objects.all()
    
    if (request.user != room.host):
        return HttpResponse("No permission")
    
    if (request.method == 'POST'):
        # create topic in database if it doesn't exist
        topic_name = request.POST.get('room_topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('room_name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save() # save update
        return redirect('home')
        
    context = {
        'form': form,
        'topics': topics,
        'room': room,
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

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    
    if (request.method == 'POST'):
        form = UserForm(request.POST, instance=user)
        if (form.is_valid()):
            form.save()
            return redirect('profile', user.username)
    
    context = {
        'form': form,
    }
    
    return render(request, 'base/update_user.html', context)

def topicView(request):
    if request.GET.get('q') != None:
        q = request.GET.get('q')
        topics = Topic.objects.filter(name__icontains=q)
    else:
        topics = Topic.objects.all()
    
    context = {
        'topics': topics,
    }
    
    return render(request, 'base/topics.html', context)

def activityView(request):
    room_messages = Message.objects.all()
    
    context = {
        'room_messages': room_messages,
    }
    
    return render(request, 'base/activity.html', context)