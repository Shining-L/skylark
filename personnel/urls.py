from django.urls import path
from personnel.views import interview
urlpatterns = [
    path('interview_registration/', interview.interview_registration, name='interview_registration'),
    path('success/', interview.success, name='success'),  # 成功页面的路由
]
