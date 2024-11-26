from django import forms
from .models import InterviewRegistration

class InterviewRegistrationForm(forms.ModelForm):
    class Meta:
        model = InterviewRegistration
        fields = ['date', 'name', 'gender', 'contact', 'position', 'interviewer', 'channel']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'name': forms.TextInput(attrs={'placeholder': '请输入姓名'}),
            'gender': forms.Select(choices=[('', '请选择性别'), ('男', '男'), ('男', '女')]),
            'contact': forms.TextInput(attrs={'placeholder': '请输入联系方式'}),
            'position': forms.Select(choices=[('', '请选择岗位'), ('开发岗位', '开发岗位'), ('课程顾问', '课程顾问'), ('售前讲师', '售前讲师'), ('售后班主任', '售后班主任'), ('售后讲师','售后讲师'), ('运营', '运营')]),
            'interviewer': forms.TextInput(attrs={'placeholder': '请输入约面人'}),
            'channel': forms.TextInput(attrs={'placeholder': '请输入应聘渠道'}),
        }
