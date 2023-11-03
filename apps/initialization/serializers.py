from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from apps.authentication.models import (
    Student,
    Teacher,
    Parent,
    User,
    Group,
    Lesson,
    StudentProfile,
    TeacherProfile,
    Attendance,
    Mark
)

from apps.comment.serializers import StudentCommentFromTeacherSerializer    

class AsyncLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'group', 'unite', 'grammar', 'vocabulary', 'home_work']
        read_only_fields = fields

class AdminSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    phone_number = PhoneNumberField()
    password = serializers.CharField(max_length=100)

    def create(self, validated_data):
        admin = User.objects.create_user(
            validated_data["username"],
            validated_data["phone_number"],
            validated_data["password"]
        )
        return admin


class CustomAdminForDataItSelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'is_admin', 'is_student', 'is_teacher', 'is_parent', 'get_type']


class LessonSerializer(serializers.ModelSerializer):
    group_data = serializers.SerializerMethodField(read_only=True)
    date_created = serializers.DateField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'group', 'unite', 'grammar', 'vocabulary', 'home_work', 'group_data', 'date_created']

    def get_group_data(self, obj):
        data = {
            "name": obj.group.name,
            "course_date": obj.group.course_date,
            "course_time": obj.group.course_time,
            "total_courses": obj.group.total_courses,
            "teacher": obj.group.teacher.full_name,
        }
        return data


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ['id', "student", "lesson", "mark"]


class AttendanceSerializer(serializers.ModelSerializer):
    student_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Attendance
        fields = ("id", "student", "lesson", "come", "student_data")

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["info"] = "Bu yerda come boolean type kelgan. Yani studenti keldi kettisini True, False orqali qilinadi"
        return rep

    def get_student_data(self, obj):
        data = {
            "id": obj.student.id,
            "full_name": obj.student.full_name,
            "group": obj.student.group.name
        }
        return data


class UserSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ['id', 'user_unique_id', 'phone_number', 'password', 'username', 'is_active', 'is_student',
                  'is_teacher', 'is_parent',
                  'get_type']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["password"] = instance.password
        rep["info"] = "Bu barchasi Userlarning Malumotlari"
        return rep


class ParentSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField(read_only=True)
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Parent
        fields = ["id", "full_name", "student", "user"]

    lookup_field = 'slug'
    extra_kwargs = {
        'url': {'lookup_field': 'slug'}
    }

    def get_student(self, obj):
        if obj.student is None:
            return None
        else:
            student_data = {
                "id": obj.student.id,
                "full_name": obj.student.full_name,
                "username": obj.student.user.username,
                "group": obj.student.group.name,
                "course_date": obj.student.group.course_date,
                "course_time": obj.student.group.course_time,
                "total_courses": obj.student.group.total_courses,
                "teacher": obj.student.group.teacher.full_name,
                "teacher_username": obj.student.group.teacher.user.username,
            }
            return student_data


class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = ['avatar']


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = [
            'avatar',
        ]


# create serializer to get student profile
class StudentSerializer(serializers.HyperlinkedModelSerializer):
    """
    Bu yerda studentlar ro'yxatini olish uchun serializer yaratiladi
    """
    student_profile = StudentProfileSerializer()
    user = UserSerializer(many=False)
    parent = ParentSerializer(many=True, read_only=True)
    attendances = AttendanceSerializer(many=True, read_only=True)
    marks = MarkSerializer(many=True, read_only=True)
    student_comment = StudentCommentFromTeacherSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = (
            "id",
            'full_name',
            "age",
            'student_profile',
            'user',
            'parent',
            "attendances",
            "marks",
            "get_average_mark",
            "student_comment",
        )

    lookup_field = 'slug'
    extra_kwargs = {
        'url': {'lookup_field': 'slug'}
    }

    def update(self, instance, validated_data):
        student_profile_data = validated_data.pop('student_profile', {})
        student_profile = instance.student_profile

        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.save()

        student_profile.avatar = student_profile_data.get('avatar', student_profile.avatar)
        student_profile.save()
        return instance


class TeacherSerializer(serializers.HyperlinkedModelSerializer):
    """
    Bu yerda teacherlar ro'yxatini olish uchun serializer yaratiladi
    """
    user = UserSerializer(many=False)
    teacher_profile = TeacherProfileSerializer(many=False)
    teacher_comment = StudentCommentFromTeacherSerializer(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = (
            "id",
            "full_name",
            'teacher_profile',
            'user',
            "teacher_comment"
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["info"] = "Bu yerdagi Teacherlarning Malumotlari"
        return rep

    lookup_field = 'slug'
    extra_kwargs = {
        'url': {'lookup_field': 'slug'}
    }

    def update(self, instance, validated_data):
        teacher_profile_data = validated_data.pop('teacher_profile', {})
        teacher_profile = instance.teacher_profile

        instance.full_name = validated_data.get('name', instance.full_name)
        instance.save()

        teacher_profile.avatar = teacher_profile_data.get('avatar', teacher_profile.avatar)
        teacher_profile.save()
        return instance


class GroupSerializer(serializers.ModelSerializer):
    teacher_data = serializers.SerializerMethodField(read_only=True)
    students = StudentSerializer(many=True, read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    course_date = serializers.DateField(format="%Y-%m-%d")
    course_time = serializers.TimeField(format="%H:%M")

    class Meta:
        model = Group
        fields = ['id', 'name', 'course_date', 'total_courses', 'course_time', 'lessons', 'teacher', 'teacher_data',
                  'students', 'days']

    def get_teacher_data(self, obj):
        if obj.teacher is None:
            return None
        else:
            teacher_data = {
                "id": obj.teacher.id,
                "full_name": obj.teacher.full_name,
                "username": obj.teacher.user.username,
            }
            return teacher_data
