from cadets.views import students
from django.urls import path
urlpatterns = [
    path("students/", students.StudentView.as_view(), name="students"),
]
