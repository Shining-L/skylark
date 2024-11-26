from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from cadets.models import Users, Role


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # 确保用户已认证

    def get(self, request):
        user = request.user  # 获取当前登录用户

        role = user.role  # 获取用户的角色

        if not role:
            return Response({
                "code": 1,
                "msg": "用户没有角色",
                "data": {}
            }, status=status.HTTP_400_BAD_REQUEST)

        # 获取角色的权限
        permissions = role.permissions.values_list('route', flat=True)  # 获取权限路由列表

        # 管理员数据
        super = Users.objects.get(username=user)
        if super.is_superuser == 1:
            response_data = {
                "code": 200,
                "msg": "操作成功",
                "data": {
                    "id": user.id,
                    "name": user.username,
                    "roleId": role.id,
                    "roleName": role.name,
                    "permissions": ["*:*:*"],
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)

        # 构建返回数据
        response_data = {
            "code": 200,
            "msg": "操作成功",
            "data": {
                "id": user.id,
                "name": user.username,
                "roleId": role.id,
                "roleName": role.name,
                "permissions": list(permissions),
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)
