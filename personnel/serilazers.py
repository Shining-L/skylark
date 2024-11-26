from rest_framework import serializers
from .models import InterviewRegistration

class InterViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewRegistration
        fields = '__all__'
