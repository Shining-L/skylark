import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cadets.models import StudentManage
from cadets.serializers import StudentManageSerializer


class StudentView(APIView):
    def get(self, request):
        # 查询所有学生信息
        stu_all = StudentManage.objects.all()

        # 使用序列化器将查询结果转换为可序列化的格式
        serializer = StudentManageSerializer(stu_all, many=True)

        # 构建响应数据
        res = {
            "code": 200,
            "message": "success",
            "data": serializer.data
        }

        # 返回HTTP响应
        return Response(res)

    def post(self, request):
        res = {
            'code': 200,
            'msg': 'success',
            'data': {}
        }
        StudentManage.objects.create(**request.data)
        return Response(res)
    def put(self, request):
        # 处理PUT请求的逻辑
        pass

    def delete(self, request):
        # 处理DELETE请求的逻辑
        pass
