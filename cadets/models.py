from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    gender_choices = (
        (0, '男'),
        (1, '女'),
        (2, '保密')
    )

    name = models.CharField(verbose_name='姓名', max_length=32, null=True)
    gender = models.IntegerField(verbose_name='性别', choices=gender_choices, null=True, default=2)
    age = models.IntegerField(verbose_name='年龄', null=True)
    phone = models.CharField(verbose_name='手机号', max_length=32, null=True)
    role = models.ForeignKey(
        to="Characters",
        verbose_name="角色",
        to_field="id",
        on_delete=models.SET_NULL, null=True, blank=True)

class Characters(models.Model):
    name = models.CharField(verbose_name="角色名称", max_length=64)
    note = models.TextField(verbose_name="备注", null=True)
    status = models.IntegerField(choices=((0, '禁用'), (1, '启用')), verbose_name="角色状态", null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, null=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True, null=True)

    class Meta:
        db_table = "characters"
        verbose_name = "角色"
        verbose_name_plural = verbose_name


class LearningStatus(models.IntegerChoices):
    NORMAL = 0, '正常'
    TRANSFERRED_IN = 1, '转入'
    TRANSFERRED_OUT = 2, '转出'
    SUSPENDED = 3, '休学'
    REFUNDED = 4, '退款'


# 创建学生管理模型，用于存储学生的详细信息
class StudentManage(models.Model):
    # 学习状态，字符型字段，最大长度为50，限制输入为LearningStatus中定义的选择项
    learning_status = models.IntegerField(choices=LearningStatus.choices)

    # 报名日期，日期字段，用于记录学生报名课程的具体日期
    registration_date = models.DateField(null=True, blank=True)

    # 学生姓名，字符型字段，最大长度为50
    name = models.CharField(max_length=100, null=True, blank=True)

    # 微信昵称，字符型字段，最大长度为50
    wechat_nickname = models.CharField(max_length=100, null=True, blank=True)

    # 电话号码，字符型字段，最大长度为20，用于存储学生的联系方式
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    # 年龄，整数型字段，用于记录学生的年龄
    age = models.IntegerField(null=True, blank=True)

    # 应付金额，十进制字段，最大10位数字，其中包含2位小数点后的数字，用于记录学生应付的总费用
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # 已付金额，十进制字段，最大10位数字，其中包含2位小数点后的数字，用于记录学生已支付的费用
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # 欠款金额，十进制字段，最大10位数字，其中包含2位小数点后的数字，用于记录学生未支付的余额
    amount_outstanding = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # 接待，字符型字段，最大长度为50，用于记录接待学生的工作人员
    receptionist = models.CharField(max_length=50, null=True, blank=True)

    # 班主任，字符型字段，最大长度为50，用于记录负责该学生的教师
    class_teacher = models.CharField(max_length=50, null=True, blank=True)

    # 讲师，字符型字段，最大长度为50，用于记录教授该学生的讲师
    lecturer = models.CharField(max_length=50, null=True, blank=True)

    # 课程名称，字符型字段，最大长度为100，用于记录学生所选的课程名称
    course_name = models.CharField(max_length=100, null=True, blank=True)

    # 服务记录图像，图像字段，上传到'service_record_images'目录下，允许为空和不上传
    service_record_image = models.TextField(null=True, blank=True)

    # 提交人
    submitter = models.ForeignKey(
        to="Users",
        to_field="id",
        on_delete=models.SET_NULL, null=True, blank=True)

    # 特殊备注
    desc = models.TextField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "student_manage"
        verbose_name = "学员管理"
        verbose_name_plural = verbose_name

        index_together = ["name", "phone_number"]
