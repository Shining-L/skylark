from cadets.views import students, users, personal
from django.urls import path, include
from .views import MyObtainTokenPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
        )


urlpatterns = [
    # 获取Token的接口
    path('login/', MyObtainTokenPairView.as_view(), name='login'),
    # 刷新Token有效期的接口
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 验证Token的有效性
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # 用户接口
    path('user/', users.UserView.as_view()),
    path('personal/', personal.PersonalView.as_view()),
    # 学员相关
    path('cadets/', students.StudentView.as_view(), name='cadets'),
    ]
