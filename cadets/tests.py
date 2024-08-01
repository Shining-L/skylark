from django.test import TestCase
from .models import Users, Characters, StudentManage, LearningStatus
from datetime import date


class ModelTests(TestCase):

    def setUp(self):
        # 创建Characters实例
        self.character = Characters.objects.create(
            name="Test Character",
            note="This is a test character."
        )

        # 创建Users实例
        self.user = Users.objects.create_user(
            username='testuser',
            password='testpass',
            name='Test User',
            gender='Male',
            age=30,
            phone='1234567890',
            role=self.character
        )

    def test_studentmanage_creation(self):
        # 创建StudentManage实例
        registration_date = date(2023, 1, 1)
        student = StudentManage.objects.create(
            learning_status=LearningStatus.NORMAL,
            registration_date=registration_date,
            name='Test Student',
            wechat_nickname='Test Nickname',
            phone_number='0987654321',
            age=25,
            amount_due=1000.00,
            amount_paid=500.00,
            amount_outstanding=500.00,
            receptionist='Receptionist Name',
            class_teacher='Class Teacher Name',
            lecturer='Lecturer Name',
            course_name='Test Course',
            submitter=self.user,
            desc='Additional description'
        )

        # 断言检查
        self.assertEqual(student.learning_status, LearningStatus.NORMAL)
        self.assertEqual(student.registration_date.year, 2023)
        self.assertEqual(student.name, 'Test Student')
        self.assertEqual(student.age, 25)
        self.assertEqual(student.amount_due, 1000.00)
        self.assertEqual(student.receptionist, 'Receptionist Name')
        self.assertEqual(student.submitter, self.user)
        self.assertEqual(student.desc, 'Additional description')

    def test_users_creation(self):
        # 在setUp中已经创建了用户，这里可以直接使用
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.name, 'Test User')
        self.assertEqual(self.user.gender, 'Male')
        self.assertEqual(self.user.age, 30)
        self.assertEqual(self.user.phone, '1234567890')
        self.assertEqual(self.user.role, self.character)

    def test_characters_creation(self):
        # 在setUp中已经创建了角色，这里可以直接使用
        self.assertEqual(self.character.name, "Test Character")
        self.assertEqual(self.character.note, "This is a test character.")
