from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.paginator import Paginator
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

        page = request.query_params.get('page', '1')
        pageSize = request.query_params.get('pageSize', '10')

        users = Users.objects.filter(role=role)

        paginator = Paginator(users, int(pageSize))
        current_page = paginator.page(int(page))

        serializer = UserSerializer(current_page.object_list, many=True)

        response_data = {
            "code": 1000,
            "msg": "获取成功",
            "data": {
                "total": paginator.count,
                "rows": serializer.data
            }
        }

        return Response(response_data)
