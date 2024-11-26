from rest_framework.views import APIView
from rest_framework.response import Response
from personnel.models import InterviewRegistration
from personnel.serilazers import InterViewSerializer
from django.db.models import Q
from api.config.pagination import Pagination
from rest_framework import status

class InterView(APIView):
    def get(self, request):
        data = {
            'code': 1000,
            'msg': '获取数据成功！',
            'data': [],
            'total': 0
        }

        name = request.GET.get('name')
        phone = request.GET.get('phone')

        currentPage = request.GET.get('page', 1)  # 设置默认值为1
        pageSize = request.GET.get('pageSize', 10)  # 设置默认值为10

        query_params = Q()

        if name:
            query_params &= Q(name__icontains=name)

        if phone:
            query_params &= Q(contact__icontains=phone)

        queryset = InterviewRegistration.objects.filter(query_params)

        count = queryset.count()
        data['total'] = count

        # 确保将 currentPage 和 pageSize 转换为整数
        pager = Pagination(all_count=int(count), current_page=int(currentPage), limit=int(pageSize))
        inter_list = queryset[pager.start:pager.end]

        # 使用序列化器序列化数据
        pag_queryset = InterViewSerializer(inter_list, many=True)
        data['data'] = pag_queryset.data

        return Response(data)

    def post(self, request):
        # 处理日期格式
        if 'date' in request.data:
            request.data['date'] = request.data['date'][:10]  # 确保日期格式为 YYYY-MM-DD

        serializer = InterViewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': 200,
                'msg': '添加成功！',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'code': 400,
            'msg': '添加失败！',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            interview = InterviewRegistration.objects.get(pk=pk)
        except InterviewRegistration.DoesNotExist:
            return Response({
                'code': 404,
                'msg': '记录未找到！'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = InterViewSerializer(interview, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': 200,
                'msg': '更新成功！',
                'data': serializer.data
            })
        return Response({
            'code': 400,
            'msg': '更新失败！',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            interview = InterviewRegistration.objects.get(pk=pk)
            interview.delete()
            return Response({
                'code': 200,
                'msg': '删除成功！'
            })
        except InterviewRegistration.DoesNotExist:
            return Response({
                'code': 404,
                'msg': '记录未找到！'
            }, status=status.HTTP_404_NOT_FOUND)
