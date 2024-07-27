from rest_framework import viewsets
from rest_framework.response import Response
from cadets.serializers import StudentManageSerializer
from cadets.models import StudentManage

class StudentView(viewsets.ModelViewSet):
    queryset = StudentManage.objects.all()
    serializer_class = StudentManageSerializer

