from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer
from base.api import serializers

@api_view(['GET', 'POST'])
def getRoutes(request):
    routes = [
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]
    return Response(routes)

@api_view(['GET', 'POST'])
def getRooms(request):
    rooms = Room.objects.all()
    # serialize room objects
    serializer = RoomSerializer(rooms, many=True)
    
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def getRoom(request, roomID):
    room = Room.objects.get(id=roomID)
    # serialize room objects
    serializer = RoomSerializer(room)
    
    return Response(serializer.data)