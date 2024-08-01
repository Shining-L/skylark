from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from cadets.serializers import LoginSerializer
from datetime import timedelta

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            remember_me = request.data.get('remember_me', False)
            if remember_me:
                refresh_token = RefreshToken.for_user(user).set_exp(timedelta(days=15))
            else:
                # 默认有效期
                refresh_token = RefreshToken.for_user(user)
            token = str(refresh_token.access_token)
            return Response({'token': token}, status=status.HTTP_200_OK)
        else:
            # 输入数据不符合要求
            return Response({'msg': '用户名或密码错误'}, status=status.HTTP_400_BAD_REQUEST)