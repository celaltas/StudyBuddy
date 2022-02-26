from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.api import serializers
from base.models import Room
from .serializers import RoomSerilazer


@api_view(['GET'])
def get_routes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]

    return Response(routes)

@api_view(['GET'])
def get_rooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerilazer(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_room(request,pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerilazer(room, many=False)
    return Response(serializer.data)
