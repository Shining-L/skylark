from cadets.views import students, users
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', users.UsersViewSet)
router.register(r'characters', users.CharactersViewSet)
router.register(r'students', students.StudentView)
urlpatterns = [
    path('', include(router.urls))
    ]
