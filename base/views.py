from email import message
from multiprocessing import context
from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Q
from .models import Room, Topic, Message
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm



def home(request):
    q = request.GET.get('q') or ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    )
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'q': q,
        'room_messages':room_messages
    }

    return render(request, 'base/home.html', context=context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants,
    }
    return render(request, 'base/room.html', context=context)


@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')
    context = {
        'form': form,
    }
    return render(request, 'base/room_form.html', context=context)


@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not allowed to update this room")

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'form': form,
    }
    return render(request, 'base/room_form.html', context=context)


@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You are not allowed to update this room")

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {
        'obj': room
    }
    return render(request, 'base/delete.html', context=context)


def login_page(request):

    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request=request, message='User does not exists')

        user = authenticate(
            request=request, username=username, password=password)
        if user is not None:
            login(request=request, user=user)
            return redirect('home')
        else:
            messages.error(request=request,
                           message='Username or password does not exists')

    context = {
        'page': page
    }
    return render(request, 'base/login_register.html', context=context)


def logout_page(request):
    logout(request=request)
    return redirect('home')


def register_page(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request=request, user=user)
            return redirect('home')
        else:
            messages.error(request=request, message="An error occured during registration")
    context = {
            'page': page,
            'form': form,
        }
    return render(request, 'base/login_register.html', context=context)




@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You are not allowed to update this room")

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    context = {
        'obj': message
    }
    return render(request, 'base/delete.html', context=context)





def user_profile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    
    context={
        'user':user,
        'rooms':rooms,
        'topics':topics,
        'room_messages':room_messages,
    }
    return render(request, 'base/profile.html', context=context)