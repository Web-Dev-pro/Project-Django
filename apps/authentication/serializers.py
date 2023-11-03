from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer

from .models import (
    User,
    Teacher,
    Student,
    Parent,
    Group,
)
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField


class CustomUserSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(region="UZ", required="True")

    class Meta:
        model = User
        fields = ['phone_number']


class ParentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Parent
        fields = ['full_name', 'student', 'user']


class CustomLoginSerializer(LoginSerializer):
    email = None
    phone_number = PhoneNumberField(region="UZ", required="True")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("username")

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        password = attrs.get("password")

        user = User.objects.filter(phone_number=phone_number).first()

        if user:
            if user.check_password(password):
                attrs["user"] = user
                attrs["backend"] = "django.contrib.auth.backends.ModelBackend"
            else:
                raise serializers.ValidationError("Incorrect password")

        else:
            raise serializers.ValidationError("User does not exist")

        return attrs


class CustomTeacherRegistrationSerializer(RegisterSerializer):
    user = CustomUserSerializer()
    full_name = serializers.CharField(max_length=100)
    email = None

    def get_cleaned_data(self):
        data = super(CustomTeacherRegistrationSerializer, self).get_cleaned_data()
        confirm_data = {
            "full_name": self.validated_data.get("full_name", ""),
        }

        data.update(confirm_data)
        return data

    def save(self, request):
        user = super(CustomTeacherRegistrationSerializer, self).save(request)
        user.is_teacher = True
        user.save()

        user_data = self.validated_data.get("user", {})
        phone_number = user_data.get("phone_number", "")

        user.phone_number = phone_number
        user.save()

        teacher = Teacher(
            user=user,
            full_name=self.cleaned_data.get("full_name"),
        )
        teacher.save()
        return user


class CustomParentRegistrationSerializer(RegisterSerializer):
    email = None
    full_name = serializers.CharField(max_length=100)
    user = CustomUserSerializer()

    def get_cleaned_data(self):
        data = super(CustomParentRegistrationSerializer, self).get_cleaned_data()
        confirm_data = {
            "full_name": self.validated_data.get("full_name", ""),
        }
        data.update(confirm_data)
        return data

    def save(self, request):
        user = super(CustomParentRegistrationSerializer, self).save(request)
        user.is_parent = True
        user.save()

        user_data = self.validated_data.get("user", {})
        phone_number = user_data.get("phone_number", "")
        user.phone_number = phone_number
        user.save()

        # get one student last created and assign to parent
        student = Student.objects.last()

        parent = Parent(
            user=user,
            student=student,
            full_name=self.cleaned_data.get("full_name"),
        )
        parent.save()
        return user


class CustomStudentRegistrationSerializer(RegisterSerializer):
    email = None
    full_name = serializers.CharField(max_length=100)
    age = serializers.IntegerField()
    user = CustomUserSerializer()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["group_name"] = serializers.ChoiceField(choices=self.get_group_choices())


    def get_group_choices(self):
        return [(group.name, group.name) for group in Group.objects.all()]

    def get_cleaned_data(self):
        data = super(CustomStudentRegistrationSerializer, self).get_cleaned_data()
        confirm_data = {
            "full_name": self.validated_data.get("full_name", ""),
            "age": self.validated_data.get("age", ""),
        }
        data.update(confirm_data)
        return data

    def save(self, request):
        user = super().save(request)
        user.is_student = True
        user.save()

        user_data = self.validated_data.get("user", {})
        phone_number = user_data.get("phone_number", "")
        user.phone_number = phone_number
        user.save()

        group_name = self.validated_data.get("group_name")
        group = Group.objects.get(name=group_name)

        student = Student.objects.create(
            user=user,
            group=group,
            full_name=self.cleaned_data.get("full_name"),
            age=self.cleaned_data.get("age"),
        )
        return user
