from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
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


class UpdatePasswordView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        # 进行密码修改逻辑
        if new_password != confirm_password:
            return Response({"msg": "新密码与确认密码不匹配"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        if not user.check_password(old_password):
            return Response({"msg": "旧密码不正确"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"msg": "密码更新成功"}, status=status.HTTP_200_OK)
