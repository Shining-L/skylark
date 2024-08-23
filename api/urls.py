from cadets.views import (students,
                          users,
                          personal,batch,hd_file, roles, sk_permission)
from django.urls import path, include
from .views import login, u_role,rest

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
        )


urlpatterns = [
    # 获取Token的接口
    path('login/', login.MyObtainTokenPairView.as_view(), name='login'),
    # 刷新Token有效期的接口
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 验证Token的有效性
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # 用户接口
    path('user/', users.UserView.as_view()),
    path('user/<int:pk>', users.UserView.as_view()),
    path('user/reset_password/<int:pk>/', rest.ResetPasswordView.as_view(), name='reset_password'),

    path('personal/', personal.PersonalView.as_view()),
    # 角色接口
    path('roles/', roles.CharacterList.as_view()),
    path('role/<int:pk>',roles.CharacterDetail.as_view()),
    path('roleUser/<int:pk>', u_role.RoleUserView.as_view()),
    path('menus/', sk_permission.GetPermissionsTreeView.as_view()),
    # 学员相关
    path('cadets/', students.StudentView.as_view(), name='cadets-list-create'),
    # PUT, PATCH, DELETE
    path('cadets/<int:pk>/', students.StudentView.as_view(), name='cadets-detail'),
    path('cadets/batch-delete/', batch.BatchDeleteView.as_view(), name='batch-delete'),
    # csv
    path('upload_csv/', hd_file.UploadFile.as_view(), name='upload_csv'),
]
