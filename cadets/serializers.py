from rest_framework import serializers
from .models import Users, Characters
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_skylark_backend import settings

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user, remember_me=False):
        refresh_token = RefreshToken.for_user(user)

        # 如果选择了“记住我”，则设置更长的过期时间
        if remember_me:
            refresh_token.set_exp(settings.SIMPLE_JWT['REFRESH_TOKEN_EXPIRE_REMEMBER_ME'])

        return refresh_token

    def validate(self, attrs):
        data = super().validate(attrs)
        remember_me = attrs.get('remember', False)
        refresh = self.get_token(self.user, remember_me)
        data['refresh'] = str(refresh)
        data['token'] = str(refresh.access_token)
        data['username'] = self.user.username

        if remember_me:
            data['expires_in'] = settings.SIMPLE_JWT['REFRESH_TOKEN_EXPIRE_REMEMBER_ME']

        return data

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.name', read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ['id', 'name', 'gender', 'age', 'phone', 'role', 'password', 'username']
        extra_kwargs = {'password': {'write_only': True}}

class CharactersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characters
        fields = '__all__'