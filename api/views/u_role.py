from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from cadets.models import Users, Role
from cadets.serializers import UserSerializer


class RoleUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            role = Role.objects.get(id=pk)
        except Role.DoesNotExist:
            return Response({
                "code": 1001,
                "msg": "角色不存在",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)

        users = Users.objects.filter(role=role)

        serializer = UserSerializer(users, many=True)

        response_data = {
            "code": 1000,
            "msg": "获取成功",
            "data": {
                "total": users.count(),
                "rows": serializer.data
            }
        }

        return Response(response_data)
