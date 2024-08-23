from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from cadets.models import Users, Role
from cadets.serializers import UserSerializer
from api.config.pagination import Pagination
from django.contrib.auth.hashers import make_password


class UserView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request, pk=None):
        if pk:
            user = Users.objects.filter(id=pk).first()
            if user:
                serializer = UserSerializer(user)
                return Response({
                    "code": 0,
                    "msg": "success",
                    "data": serializer.data
                })
            else:
                return Response({"msg": "用户不存在"}, status=status.HTTP_404_NOT_FOUND)
        else:
            name = request.GET.get('name')
            currentPage = request.GET.get('page') or 1
            pageSize = request.GET.get('pageSize') or 10

            if name:
                user_query = Users.objects.filter(name__contains=name)
            else:
                user_query = Users.objects.all()
            total = user_query.count()
            pager = Pagination(limit=int(pageSize), all_count=int(total), current_page=int(currentPage))

            user_list = user_query[pager.start: pager.end]
            serializer = UserSerializer(instance=user_list, many=True)

            return Response({
                "code": 0,
                "msg": "success",
                "data": {
                    "total": total,
                    "rows": serializer.data
                }
            })

    def post(self, request):
        username = request.data.get('userName')
        password = request.data.get('password')
        name = request.data.get('name')  # 获取员工姓名
        phonenumber = request.data.get('phonenumber')  # 获取联系方式
        roleId = request.data.get('roleId')

        # 验证用户名是否已存在
        if Users.objects.filter(username=username).exists():
            return Response({"msg": "用户名已存在"}, status=status.HTTP_400_BAD_REQUEST)

        # 验证密码
        if not password or len(password) < 6:
            return Response({'msg': '密码必须至少6个字符'}, status=status.HTTP_400_BAD_REQUEST)

        # 获取角色
        role = Role.objects.filter(id=roleId).first()
        if not role:
            return Response({'msg': '指定的角色不存在'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = Users.objects.create(
                username=username,
                password=make_password(password),  # 使用make_password确保密码被正确哈希
                role=role,
                is_active=True,
                name=name,
                phone=phonenumber
            )
            serializer = UserSerializer(instance=user)
            return Response({
                "code": 0,
                "msg": "用户添加成功",
                "data": {
                    "total": 1,
                    "rows": [serializer.data]
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "msg": f'添加用户时发生错误: {str(e)}',
                "data": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk=None):
        if pk:
            user = Users.objects.filter(id=pk).first()
            if not user:
                return Response({'msg': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)

            serializer = UserSerializer(instance=user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "code": 0,
                    "msg": "编辑成功",
                    "data": serializer.data
                })
            else:
                return Response({
                    "msg": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "未提供用户 ID"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if pk:
            user_query = Users.objects.filter(id=pk)
            if user_query.exists():
                user_query.delete()
                return Response({
                    "code": 0,
                    "msg": "用户已删除"
                }, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'msg': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"msg": "未提供用户 ID"}, status=status.HTTP_400_BAD_REQUEST)


