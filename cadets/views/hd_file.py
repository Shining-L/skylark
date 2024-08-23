from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from utils.handle_files import save_file


class UploadFile(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        # 检查是否有文件上传
        file = request.FILES.get('file')
        if not file:
            return Response({'status': 'error', 'message': '没有上传文件'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 调用 save_file 函数处理上传的文件
            result = save_file(file, request)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
