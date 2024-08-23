from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from cadets.models import Users

class ResetPasswordView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request, pk=None):
        user = Users.objects.filter(id=pk).first()
        if not user:
            return Response({'msg': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)

        user.set_password('123456')
        user.save()
        return Response({"code": 0, "msg": "密码已重置为 123456"}, status=status.HTTP_200_OK)
