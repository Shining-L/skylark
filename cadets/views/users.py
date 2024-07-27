from rest_framework import viewsets
from cadets.models import Users, Characters
from cadets.serializers import UserSerializer, CharactersSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

class CharactersViewSet(viewsets.ModelViewSet):
    queryset = Characters.objects.all()
    serializer_class = UserSerializer
