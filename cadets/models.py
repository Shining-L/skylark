from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    status_choice = (
        (0, "禁用"),
        (1, "启用")
    )
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
        to="Role",
        verbose_name="角色",
        to_field="id",
        on_delete=models.SET_NULL, null=True, blank=True)
    status = models.IntegerField(choices=status_choice, default=1)

class PermissionGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Permission(models.Model):
    name = models.CharField(max_length=50)
    group = models.ForeignKey(PermissionGroup, on_delete=models.CASCADE, related_name='permissions')
    route = models.CharField(max_length=255, unique=True, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        if self.parent:
            return f"{self.group.name} - {self.parent.name} - {self.name}"
        else:
            return f"{self.group.name} - {self.name}"


class Role(models.Model):
    name = models.CharField(max_length=50)
    remark = models.CharField(max_length=50,null=True)
    permissions = models.ManyToManyField(Permission, through='RolePermission')

    def __str__(self):
        return self.name


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('role', 'permission')

    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"


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

    # 服务记录图像，图像字段，
    service_record_images = models.JSONField(blank=True, default=list)
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

        indexes = [
            models.Index(fields=['name', 'phone_number']),
        ]
