from rest_framework.views import APIView
from rest_framework.response import Response
from cadets.models import StudentManage
from api.config.pagination import Pagination


class StudentView(APIView):
    def get(self, request):
        res = {
            'code': 200,
            'msg': 'success',
            'data': []
        }

        # 分页配置
        page = request.query_params.get('page')
        size = request.query_params.get('size')
        total = StudentManage.objects.count()

        # 搜索配置
        name = request.query_params.get('name') or ''
        phone_number = request.query_params.get('phone')

        # 过滤查询条件
        filters = {}

        if name:
            filters['name__contains'] = name

        if phone_number:
            filters['phone_number'] = phone_number

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
                'submitter': student.submitter.name,
                'desc': student.desc
            })
        res['total'] = total
        return Response(res)
