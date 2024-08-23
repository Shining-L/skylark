from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cadets.models import Role
from cadets.serializers import CharactersSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import NotFound

class CharacterList(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        characters = Role.objects.all()
        serializer = CharactersSerializer(characters, many=True)
        return Response({'msg': '操作成功', 'data': serializer.data}, status=200)

    def post(self, request):
        role_data = request.data.copy()
        permissions = role_data.pop('perms', [])

        flat_permissions = []
        for perm_group in permissions:
            if isinstance(perm_group, list):
                flat_permissions.extend(perm_group)
            else:
                flat_permissions.append(perm_group)

        serializer = CharactersSerializer(data=role_data)
        if serializer.is_valid():
            role = serializer.save()

            # 确保permissions是一个整数列表
            permissions_to_set = [int(perm) for perm in flat_permissions if str(perm).isdigit()]

            role.permissions.set(permissions_to_set)

            # 重新获取角色数据，包括权限
            updated_role = CharactersSerializer(role).data
            updated_role['permissions'] = list(role.permissions.values_list('id', flat=True))

            return Response({'msg': '操作成功', 'data': updated_role}, status=status.HTTP_201_CREATED)
        return Response({'msg': '操作失败', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class CharacterDetail(APIView):
    authentication_classes = [JWTAuthentication]


    def get(self, request, pk):
        try:
            role = Role.objects.get(pk=pk)
            serializer = CharactersSerializer(role)
            return Response({
                'msg': '操作成功',
                'data': serializer.data
            })
        except Role.DoesNotExist:
            raise NotFound(detail="角色不存在")

    def put(self, request, pk):
        try:
            role = Role.objects.get(pk=pk)
            serializer = CharactersSerializer(role, data=request.data)

            if serializer.is_valid():
                serializer.save()

                # 更新角色的权限
                permissions = request.data.get('perms', [])
                print("Received permissions:", permissions)

                # 处理可能的嵌套列表
                flat_permissions = []
                for perm in permissions:
                    if isinstance(perm, list):
                        flat_permissions.extend(perm)
                    else:
                        flat_permissions.append(perm)

                print("Flattened permissions:", flat_permissions)
                role.permissions.set(flat_permissions)  # 使用 set() 更新多对多关系

                return Response({
                    'msg': '更新成功',
                    'data': serializer.data
                })
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Role.DoesNotExist:
            raise NotFound(detail="角色不存在")
        except Exception as e:
            print("Error:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            role = Role.objects.get(pk=pk)
            role.delete()
            return Response({'msg': '删除成功'}, status=status.HTTP_200_OK)
        except Role.DoesNotExist:
            raise NotFound(detail="角色不存在")
