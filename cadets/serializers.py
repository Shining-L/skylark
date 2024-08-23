from .models import Users, Role
import pytz
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers

from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        refresh_token = RefreshToken.for_user(user)
        return refresh_token

    def validate(self, attrs):
        print(f"尝试验证用户: {attrs.get('username')}")

        # 使用authenticate函数进行用户验证
        user = authenticate(username=attrs.get('username'), password=attrs.get('password'))

        if user is None:
            print(f"用户验证失败: {attrs.get('username')}")
            raise serializers.ValidationError("无法找到具有给定凭据的活动账户")

        if not user.is_active:
            print(f"用户账户未激活: {user.username}")
            raise serializers.ValidationError("您的账户已被禁用，无法登录。")

        print(f"用户验证成功: {user.username}")

        self.user = user
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['token'] = str(refresh.access_token)
        data['username'] = self.user.username

        return data

class UserSerializer(serializers.ModelSerializer):
    roleName = serializers.CharField(source='role.name', required=False, allow_null=True)
    roleId = serializers.IntegerField(source='role.id', required=False, allow_null=True)
    userName = serializers.CharField(source='username')
    phonenumber = serializers.CharField(source='phone')
    create_time = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ['id', 'name', 'phonenumber', 'roleId','roleName', 'status', 'userName', 'create_time']

    def get_create_time(self, obj):
        # 转换为尼泊尔标准时间
        npt_timezone = pytz.timezone('Asia/Kathmandu')
        if obj.date_joined:
            return obj.date_joined.astimezone(npt_timezone).strftime('%Y-%m-%d %H:%M:%S')
        return None

    def update(self, instance, validated_data):
        # 处理 role 的更新
        role_data = validated_data.pop('role', None)
        if role_data:
            role = Role.objects.get(id=role_data['id'])
            instance.role = role

        instance.name = validated_data.get('name', instance.name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.status = validated_data.get('status', instance.status)
        instance.username = validated_data.get('username', instance.username)

        instance.save()
        return instance


class CharactersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
