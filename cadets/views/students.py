from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from cadets.models import StudentManage, Users
from api.config.pagination import Pagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.dateparse import parse_date
from django.shortcuts import get_object_or_404
from utils.handle_files import save_files
from drf_skylark_backend.settings import QINIU_SETTINGS


class StudentView(APIView):
    authentication_classes = [JWTAuthentication]  # 添加认证类

    def get(self, request, pk=None):
        res = {
            'code': 200,
            'msg': '获取数据成功！',
            'data': [],
            'total': 0
        }
        if pk is not None:
            # 获取单个学生信息
            student = get_object_or_404(StudentManage, id=pk)
            submitter_name = student.submitter.username if student.submitter else None
            data = {
                "id": student.id,
                'learning_status': student.learning_status,
                'registration_date': student.registration_date,
                'name': student.name,
                'wechat_nickname': student.wechat_nickname,
                'phone_number': student.phone_number,
                'age': student.age,
                'amount_due': student.amount_due,
                'amount_paid': student.amount_paid,
                'amount_outstanding': student.amount_outstanding,
                'receptionist': student.receptionist,
                'class_teacher': student.class_teacher,
                'lecturer': student.lecturer,
                'course_name': student.course_name,
                'service_record_images': student.service_record_images,
                'submitter': submitter_name,  # 使用 submitter_name
                'create_time': student.create_time,
                'update_time': student.update_time,
                'desc': student.desc
            }
            return Response({
                'code': 200,
                'msg': '获取数据成功！',
                'data': data
            })

        else:
            page = request.query_params.get('page', 1)  # 默认为第一页
            size = request.query_params.get('size', 10)  # 默认每页10条数据

            # 搜索配置
            name = request.query_params.get('name') or ''

            phone_number = request.query_params.get('phone') or ''
            cadets_status = request.query_params.get('learning_status') or ''

            # 过滤查询条件
            filters = {}

            if name:
                filters['name__contains'] = name

            if phone_number:
                filters['phone_number'] = phone_number

            if cadets_status:
                filters['learning_status'] = cadets_status

            # 使用过滤条件获取查询集
            queryset = StudentManage.objects.filter(**filters)

            # 使用过滤后的查询集来获取总数
            total = queryset.count()
            res['total'] = total
            # 分页逻辑
            pager = Pagination(int(page), total, int(size))
            student_list = queryset[pager.start: pager.end]

            for student in student_list:
                submitter_name = student.submitter.username if student.submitter else None
                res['data'].append({
                    "id": student.id,
                    'learning_status': student.learning_status,
                    'registration_date': student.registration_date,
                    'name': student.name,
                    'wechat_nickname': student.wechat_nickname,
                    'phone_number': student.phone_number,
                    'age': student.age,
                    'amount_due': student.amount_due,
                    'amount_paid': student.amount_paid,
                    'amount_outstanding': student.amount_outstanding,
                    'receptionist': student.receptionist,
                    'class_teacher': student.class_teacher,
                    'lecturer': student.lecturer,
                    'course_name': student.course_name,
                    'service_record_images': f"https://{QINIU_SETTINGS['host']}/{student.service_record_images[0]}" if student.service_record_images else None,
                    'submitter': submitter_name,  # 使用 submitter_name
                    'create_time': student.create_time,
                    'update_time': student.update_time,
                    'desc': student.desc
                })

            return Response(res)

    def post(self, request):
        # 从请求体中提取数据
        data = request.data
        files = request.FILES.getlist('service_record_images')

        submitter_id = request.user.id
        submitter = get_object_or_404(Users, id=submitter_id)

        # 处理日期字段
        registration_date = data.get('registration_date')
        if registration_date:
            registration_date = parse_date(registration_date)

        # 处理文件上传
        image_urls = []
        for file in files:
            # 调用一个方法处理文件保存
            ret = save_files(file)
            image_urls.append(ret['key'])
        # 创建一个新的学生对象
        try:
            student = StudentManage(
                name=data['name'],
                phone_number=data['phone_number'],
                learning_status=data['learning_status'],
                wechat_nickname=data.get('wechat_nickname', ''),
                age=data.get('age', 0),
                amount_due=data.get('amount_due', 0),
                amount_paid=data.get('amount_paid', 0),
                amount_outstanding=data.get('amount_outstanding', 0),
                receptionist=data.get('receptionist', ''),
                class_teacher=data.get('class_teacher', ''),
                lecturer=data.get('lecturer', ''),
                course_name=data.get('course_name', ''),
                service_record_images=image_urls,
                submitter=submitter,  # 使用处理后的 submitter
                desc=data.get('desc', ''),
                registration_date=registration_date,  # 使用处理后的日期
            )

            student.save()
            return Response({
                'code': 201,
                'msg': '添加成功！',
                'data': {
                    'id': student.id,  # 返回新创建的学生ID
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'code': 500,
                'msg': '添加失败！',
                'data': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk=None):
        if pk is None:
            return Response({
                'code': 400,
                'msg': '缺少学生ID！'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 从请求体中提取数据
        data = request.data
        new_files = request.FILES.getlist('new_images')
        existing_images = request.POST.getlist('existing_images')
        deleted_images = request.POST.getlist('deleted_images')

        # 获取学生对象
        student = get_object_or_404(StudentManage, id=pk)

        # 更新提交者信息
        submitter_id = request.user.id
        submitter = get_object_or_404(Users, id=submitter_id)

        # 处理日期字段
        registration_date = data.get('registration_date')
        if registration_date:
            registration_date = parse_date(registration_date)

        # 处理图片
        image_urls = []

        # 添加保留的现有图片
        image_urls.extend(existing_images)

        # 处理新上传的文件
        if new_files:
            for file in new_files:
                ret = save_files(file)
                image_urls.append(ret['key'])

        # 删除指定的图片（这里可能需要额外的逻辑来实际删除文件）
        for deleted_image in deleted_images:
            if deleted_image in image_urls:
                image_urls.remove(deleted_image)

        # 更新学生对象
        try:
            student.name = data.get('name', student.name)
            student.phone_number = data.get('phone_number', student.phone_number)
            student.learning_status = data.get('learning_status', student.learning_status)
            student.wechat_nickname = data.get('wechat_nickname', student.wechat_nickname)
            student.age = data.get('age', student.age)
            student.amount_due = data.get('amount_due', student.amount_due)
            student.amount_paid = data.get('amount_paid', student.amount_paid)
            student.amount_outstanding = data.get('amount_outstanding', student.amount_outstanding)
            student.receptionist = data.get('receptionist', student.receptionist)
            student.class_teacher = data.get('class_teacher', student.class_teacher)
            student.lecturer = data.get('lecturer', student.lecturer)
            student.course_name = data.get('course_name', student.course_name)
            student.service_record_images = image_urls
            student.submitter = submitter
            student.desc = data.get('desc', student.desc)
            student.registration_date = registration_date or student.registration_date

            student.save()
            return Response({
                'code': 200,
                'msg': '更新成功！',
                'data': {
                    'id': student.id
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'code': 500,
                'msg': '更新失败！',
                'data': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def delete(self, request, pk=None):
        # 获取要删除的学生实例
        student = get_object_or_404(StudentManage, id=pk)

        try:
            student.delete()
            return Response({
                'code': 204,
                'msg': '删除成功！'
            }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                'code': 500,
                'msg': '删除失败！',
                'data': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
