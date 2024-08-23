from rest_framework import generics, status
from rest_framework.response import Response
from cadets.models import StudentManage


class BatchDeleteView(generics.GenericAPIView):

    def delete(self, request, *args, **kwargs):
        if isinstance(request.data, dict):
            ids = request.data.get('ids')

        elif isinstance(request.data, list):
            ids = request.data

        else:
            return Response({"message": "请求数据格式错误"}, status=status.HTTP_400_BAD_REQUEST)

        if ids:
            try:
                StudentManage.objects.filter(id__in=ids).delete()
                return Response({"message": "批量删除成功"}, status=status.HTTP_204_NO_CONTENT)

            except Exception as e:
                return Response({"message": "批量删除失败", "detail": str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "未提供 ID 列表"}, status=status.HTTP_400_BAD_REQUEST)
