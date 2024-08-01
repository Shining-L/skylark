from django.core.serializers import serialize
from rest_framework import serializers
from cadets.models import StudentManage, Users, Characters
from .models import Users, Characters

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(label='用户名')
    password = serializers.CharField(label='密码', style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = Users.objects.filter(username=username).first()
        if user is not None:
            if not user.password:
                raise serializers.ValidationError('用户名或密码错误')
        else:
            # 没有找到与提供的用户名相对应的用户
            raise serializers.ValidationError('用户名或密码错误')
        attrs['user'] = user
        return attrs

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.name', read_only=True)

    class Meta:
        model = Users
        fields = ['id', 'name', 'gender', 'age', 'phone', 'role', 'password', 'username', 'is_active']

class CharactersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characters
        fields = '__all__'
