from rest_framework.views import APIView
from rest_framework.response import Response
from api.config.pagination import Pagination
from cadets.serializers import UserSerializer
from cadets.models import Users, Characters
from django.contrib.auth.hashers import make_password
from rest_framework import status

class UserView(APIView):
    def get(self, request):
        res = {
            'code': 200,
            'msg': ' success',
            'data': [],
            'total': 0
        }
        username = request.GET.get('username')
        currentPage = request.GET.get('currentPage') or 1
        pageSize = request.GET.get('pageSize') or 10

        if username:
            user_query = Users.objects.filter(username__contains=username)
        else:
            user_query = Users.objects.all()
        total = user_query.count()
        pager = Pagination(
            limit=int(pageSize),
            all_count=int(total),
            current_page=int(currentPage)
        )

        user_list = user_query[pager.start: pager.end]
        serializer = UserSerializer(instance=user_list, many=True)
        res['data'] = serializer.data
        res['total'] = total
        res['code'] = 200
        return Response(res)

    def post(self, request):
        res = {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'msg': '增加成功',
            'data': {}
        }
        role = request.data.get('role')
        char = Characters.objects.filter(name=role).first()

        username = request.data.get('username')
        password = request.data.get('password')
        # 使用 make_password 加密密码
        if password and not password.isdigit():
            hashed_password = make_password(password)

        else:
            return Response({'msg': '您的密码太常见啦'}, status=status.HTTP_400_BAD_REQUEST)

        # 判断是否是重复名
        if Users.objects.filter(username=username).exists():
            return Response({"msg": "用户名已存在"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 创建新用户
            user = Users.objects.create_user(username=username, password=hashed_password)
            user.role = char
            user.is_active = True
            user.save()
            ser = UserSerializer(instance=user, data=request.data)
            if ser.is_valid():
                ser.save()
                res['code'] = status.HTTP_200_OK
                res['data'] = ser.data
            else:
                res['msg'] = ser.errors
        return Response(res, status=status.HTTP_201_CREATED)

    def put(self, request):
        res = {
            'code': 500,
            'msg': '编辑成功',
            'data': {}
        }
        id = request.data.get('id')
        role = request.data.get('role')
        char = Characters.objects.filter(name=role).first()
        user_obj = Users.objects.filter(id=id).first()
        user_obj.role = char
        user_obj.save()
        ser = UserSerializer(instance=user_obj, data=request.data)
        if ser.is_valid():
            ser.save()
            res['code'] = 200
            res['data'] = ser.data
        else:
            res['msg'] = ser.errors
        return Response(res)

    def delete(self, request):
        id = request.query_params.get('id')
        user_query = Users.objects.filter(id=id)
        if not user_query:
            return Response({'msg':'用户不存在'},status=404)
        user_query.delete()
        return Response({})
