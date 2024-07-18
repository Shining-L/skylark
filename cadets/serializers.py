from rest_framework import serializers
from cadets.models import StudentManage, Users

class StudentManageSerializer(serializers.ModelSerializer):
    submitter = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())

    class Meta:
        model = StudentManage
        fields = '__all__'
