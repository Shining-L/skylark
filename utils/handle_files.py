import io
import pandas as pd
from qiniu import Auth, put_data
from drf_skylark_backend import settings
import csv
from cadets.models import StudentManage
from datetime import datetime
from cadets.models import LearningStatus
import json, math
from decimal import Decimal
from cadets.models import Users

def save_files(file):
    qi = settings.QINIU_SETTINGS
    q = Auth(qi['access_key'], qi['secret_key'])
    token = q.upload_token(qi['bucket_name'])

    # 上传文件到七牛云
    ret, info = put_data(token, key=None, data=file.read())

    # 检查上传结果
    if info.status_code == 200:
        return ret  # 返回包含文件信息的字典
    else:
        raise Exception(f"上传失败，状态码：{info.status_code}, 错误信息：{info.error}")


def map_learning_status(status):
    status_map = {
        '正常': LearningStatus.NORMAL,
        '转入': LearningStatus.TRANSFERRED_IN,
        '转出': LearningStatus.TRANSFERRED_OUT,
        '休学': LearningStatus.SUSPENDED,
        '退款': LearningStatus.REFUNDED
    }
    return status_map.get(status, LearningStatus.NORMAL)


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None


def preprocess_age(age_str):
    try:
        age = int(age_str)
        return age if age > 0 else None
    except (ValueError, TypeError):
        return None


def preprocess_phone_number(phone_str):
    try:
        # 如果电话号码是字符串
        if isinstance(phone_str, str):
            # 尝试将其转换为整数
            phone_number = int(phone_str)
            # 如果转换成功，返回电话号码
            return phone_number
        # 如果电话号码是浮点数
        elif isinstance(phone_str, float):
            # 检查是否为 NaN
            if math.isnan(phone_str):
                return None
            # 如果不是 NaN，尝试将其转换为整数
            phone_number = int(phone_str)
            # 如果转换成功，返回电话号码
            return phone_number
        # 如果电话号码既不是字符串也不是浮点数，则返回 None
        return None
    except (ValueError, TypeError):
        # 如果转换失败，则返回 None
        return None


def preprocess_float(value_str):
    try:
        # 尝试将字符串转换为浮点数
        value = float(value_str)
        # 检查是否为 NaN
        if math.isnan(value):
            return None
        # 如果不是 NaN，则返回 Decimal 对象
        return Decimal(str(value))
    except (ValueError, TypeError):
        # 如果转换失败，则返回 None
        return None


def is_valid_row(row):
    # 检查关键字段是否非空
    if pd.notna(row['学员姓名']) and pd.notna(row['报名日期']):
        return True
    return False


def preprocess_json(value_str):
    try:
        return json.loads(value_str) if isinstance(value_str, str) else []
    except (json.JSONDecodeError, TypeError):
        return []


def preprocess_csv_row(row, header):
    processed_row = {}
    for i, value in enumerate(row):
        column_name = header[i]
        if not pd.isnull(value):  # 只处理非空值
            if column_name == '学习状态':
                processed_row[column_name] = map_learning_status(value)
            elif column_name == '报名日期':
                processed_row[column_name] = parse_date(value)
            elif column_name == '学员姓名':
                processed_row[column_name] = value
            elif column_name == '微信昵称':
                processed_row[column_name] = value
            elif column_name == '电话号码':
                processed_row[column_name] = preprocess_phone_number(value)
            elif column_name == '年龄':
                processed_row[column_name] = preprocess_age(value)
            elif column_name == '应付金额':
                processed_row[column_name] = preprocess_float(value)
            elif column_name == '已付金额':
                processed_row[column_name] = preprocess_float(value)
            elif column_name == '欠缴金额':
                processed_row[column_name] = preprocess_float(value)
            elif column_name == '接待':
                processed_row[column_name] = value
            elif column_name == '班主任':
                processed_row[column_name] = value
            elif column_name == '讲师':
                processed_row[column_name] = value
            elif column_name == '课程名称':
                processed_row[column_name] = value
            elif column_name == '服务记录':
                processed_row[column_name] = preprocess_json(value)
    return processed_row


def save_file(file, request):
    file_content = file.read()
    submitter_id = request.user.id
    if file.name.endswith('.csv'):
        file.seek(0)
        submitter = Users.objects.get(id=submitter_id)
        csv_file = io.TextIOWrapper(io.BytesIO(file_content), encoding="utf-8")
        reader = csv.reader(csv_file)
        header = next(reader)
        for row in reader:
            try:
                processed_row = preprocess_csv_row(row, header)
                student = StudentManage(
                    phone_number=processed_row['phone_number'],
                    name=processed_row['name'],
                    learning_status=processed_row['learning_status'],
                    registration_date=processed_row['registration_date'],
                    wechat_nickname=processed_row['wechat_nickname'],
                    age=processed_row['age'],
                    amount_due=processed_row['amount_due'],
                    amount_paid=processed_row['amount_paid'],
                    amount_outstanding=processed_row['amount_outstanding'],
                    receptionist=processed_row['receptionist'],
                    class_teacher=processed_row['class_teacher'],
                    lecturer=processed_row['lecturer'],
                    course_name=processed_row['course_name'],
                    service_record_images=processed_row['service_record_images'],
                    desc=None,
                    submitter=submitter
                )
                student.save()
            except Exception as e:
                print(f"保存学生数据失败: {e}")
                continue


    elif file.name.endswith('.xlsx'):

        submitter = Users.objects.get(id=submitter_id)

        file.seek(0)

        df = pd.read_excel(io.BytesIO(file_content), parse_dates=['报名日期'])

        # 应用预处理

        df['年龄'] = df['年龄'].apply(preprocess_age)

        df['应付金额'] = df['应付金额'].apply(preprocess_float)

        df['已付金额'] = df['已付金额'].apply(preprocess_float)

        df['欠缴金额'] = df['欠缴金额'].apply(preprocess_float)

        df['服务记录'] = df['服务记录'].apply(preprocess_json)

        df['电话号码'] = df['电话号码'].apply(preprocess_phone_number)  # 应用电话号码预处理

        df['报名日期'] = df['报名日期'].apply(lambda x: x.date() if pd.notna(x) else None)

        # 过滤掉包含 NaN 的行

        # 过滤有效行
        valid_rows = [row for _, row in df.iterrows() if is_valid_row(row)]

        # 处理有效行
        for row in valid_rows:

            try:

                student = StudentManage(

                    phone_number=row.get('电话号码'),

                    name=row.get('学员姓名'),

                    learning_status=map_learning_status(row.get('学习状态')),

                    registration_date=row.get('报名日期'),

                    wechat_nickname=row.get('微信昵称'),

                    age=row.get('年龄'),

                    amount_due=row.get('应付金额'),

                    amount_paid=row.get('已付金额'),

                    amount_outstanding=row.get('欠缴金额'),

                    receptionist=row.get('接待'),

                    class_teacher=row.get('班主任'),

                    lecturer=row.get('讲师'),

                    course_name=row.get('课程名称'),

                    service_record_images=row.get('服务记录'),
                    desc=None,
                    submitter=submitter
                )

                student.save()

            except Exception as e:

                print(f"保存学生数据失败: {e}")

                continue
