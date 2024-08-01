from cadets.views import students, users
from django.urls import path, include
from rest_framework import routers
from .views import LoginView


router = routers.DefaultRouter()
router.register(r'characters', users.CharactersViewSet)
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('cadets/', students.StudentView.as_view(), name='cadets'),
    path('', include(router.urls))
    ]
