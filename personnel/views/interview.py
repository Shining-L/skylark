from django.shortcuts import render, redirect
from personnel.forms import InterviewRegistrationForm


def interview_registration(request):
    if request.method == 'POST':
        form = InterviewRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # 保存表单数据到数据库
            return redirect('success')  # 重定向到成功页面
    else:
        form = InterviewRegistrationForm()

    return render(request, 'interview_registration.html', {'form': form})


def success(request):
    return render(request, 'success.html')  # 渲染成功页面
