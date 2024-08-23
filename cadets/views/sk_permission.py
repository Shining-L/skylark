from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cadets.models import PermissionGroup, Permission


class GetPermissionsTreeView(APIView):
    def get(self, request):
        try:
            permissions_tree = self.build_permissions_tree()

            return Response({
                "code": 1000,
                "msg": "获取权限树成功",
                "data": permissions_tree
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "code": 5000,
                "msg": f"获取权限树失败: {str(e)}",
                "data": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def build_permissions_tree(self):
        tree = []
        groups = PermissionGroup.objects.all()

        for group in groups:
            group_node = {
                "id": f"group_{group.id}",
                "title": group.name,
                "children": []
            }

            top_level_permissions = Permission.objects.filter(group=group, parent=None)
            for permission in top_level_permissions:
                permission_node = self.build_permission_node(permission)
                group_node["children"].append(permission_node)

            tree.append(group_node)

        return tree

    def build_permission_node(self, permission):
        node = {
            "id": permission.id,
            "title": permission.name,
            "children": []
        }

        children = Permission.objects.filter(parent=permission)
        for child in children:
            child_node = self.build_permission_node(child)
            node["children"].append(child_node)

        return node
