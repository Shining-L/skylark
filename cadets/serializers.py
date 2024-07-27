from rest_framework import serializers
from cadets.models import StudentManage, Users, Characters


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['name', 'gender', 'age', 'phone', 'role', 'password', 'username', 'is_active']

class CharactersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characters
        fields = '__all__'

class StudentManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentManage
        fields = '__all__'
