from django.shortcuts import render, HttpResponse,redirect
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm



def home(request):
    q = request.GET.get('q') or ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)|
        Q(description__icontains=q)
        )
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {
        'rooms':rooms,
        'topics':topics,
        'room_count':room_count,
        'q':q
    }

    return render(request, 'base/home.html', context=context)


def room(request,pk):
    room = Room.objects.get(id=pk)
    return render(request, 'base/room.html', {'room':room})


def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'form':form,
    }
    return render(request, 'base/room_form.html', context=context)


def update_room(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'form':form,
    }
    return render(request, 'base/room_form.html', context=context)


def delete_room(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {
        'obj':room
    }
    return render(request, 'base/delete.html', context=context)

