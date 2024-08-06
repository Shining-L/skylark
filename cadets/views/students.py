from rest_framework.views import APIView
from rest_framework.response import Response
from cadets.models import StudentManage
from api.config.pagination import Pagination
from rest_framework_simplejwt.authentication import JWTAuthentication



class StudentView(APIView):
    authentication_classes = [JWTAuthentication]  # 添加认证类


    def get(self, request):
        res = {
            'code': 200,
            'msg': '操作成功！',
            'data': [],
            'total': 0  # 初始化 total 以避免未定义
        }

        # 分页配置
        page = request.query_params.get('page')
        size = request.query_params.get('size')
        total = StudentManage.objects.count()
        res['total'] = total  # 更新 total

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

        if page and size:
            pager = Pagination(
                int(page),
                total,
                int(size)
            )
            student_list = StudentManage.objects.filter(**filters)[pager.start: pager.end]
        else:
            student_list = StudentManage.objects.filter(**filters)

        for student in student_list:

            submitter_name = student.submitter.name if student.submitter else None
            res['data'].append({
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
                'service_record_image': student.service_record_image,
                'submitter': submitter_name,  # 使用 submitter_name
                'create_time': student.create_time,
                'update_time': student.update_time,
                'desc': student.desc
            })

        return Response(res)
