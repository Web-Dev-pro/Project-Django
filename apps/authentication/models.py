import random

from PIL import Image
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField

from django.db.models import Avg

class UserManager(BaseUserManager):

    def create_user(self, username, phone_number, password=None):
        if not password:
            raise ValueError('Parol kiritishingiz zarur yoki noto\'g\'ri parol kiritdingiz')
        if not phone_number:
            raise ValueError('Telefon raqam kiritishingiz zarur')
        if not username or len(username) <= 4:
            raise ValueError('Username kiritishingiz zarur yoki username 4 ta belgidan kam bo\'lmasligi kerak')

        user = self.model(
            username=username,
            phone_number=phone_number
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone_number, password=None):
        user = self.create_user(
            username=username,
            phone_number=phone_number,
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True, db_index=True)
    phone_number = PhoneNumberField(null=True, unique=True)
    user_unique_id = models.IntegerField(unique=True, null=True)
    # verification va qo'shimcha type uchun
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    @staticmethod
    def _generate_unique_id():
        return random.randint(100000, 999999)

    def save(self, *args, **kwargs):
        """
        Implementation of creating unique id for each user -- lets define each line of code
        1. if user_unique_id is not defined, then get all user_unique_id from User model
        2. ids = User.objects.values_list('user_unique_id', flat=True)
        above line of code will return all user_unique_id in list, flat means return list of values
        and no other sub list [[1, 2, 3, 4, 5]] -> [1, 2, 3, 4, 5] this is what flat means
        3. generate unique id
        4. if generated unique id is in ids, then generate again until it is not in ids
        5. generated unique id is not in ids, then assign it to user_unique_id
        6. super().save(*args, **kwargs) -> save user
        """
        if not self.user_unique_id:
            ids = User.objects.values_list('user_unique_id', flat=True)
            unique_id = self._generate_unique_id()
            while unique_id in ids:
                unique_id = self._generate_unique_id()
            self.user_unique_id = unique_id
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Implementation of __str__ method to show username and full name of user
        1. if user is teacher, then show username and full name of teacher
        2. if user is student, then show username and full name of student
        3. if user is parent, then show username and full name of parent
        4. if user is admin, then show username
        5. if user is not any of above, then show username
        hasattr(self, "checked item") -> here we check if user has teacher, student or parent object
        """
        if self.is_teacher:
            if hasattr(self, 'teacher'):
                return f"{self.username} -- {self.teacher.full_name}"
            else:
                return f"{self.username} -- Teacher (No associated teacher object)"
        elif self.is_student:
            if hasattr(self, 'student'):
                return f"{self.username} -- {self.student.full_name}"
            else:
                return f"{self.username} -- Student (No associated student object)"
        elif self.is_parent:
            if hasattr(self, 'parent'):
                return f"{self.username} -- {self.parent.full_name}"
            else:
                return f"{self.username} -- Parent (No associated parent object)"
        return self.username

    def token(self):
        """
        Agar token bilan ishalmoqchi bo'lsak kerak bo'ladi,
        o'chirib yuborsak zarar bermaydi:: fikriz?
        """
        return ""

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_absolute_url(self):
        """
        Userning profilega o'tish uchun
        """
        return reverse('user:detail', kwargs={'slug': self.pk})

    # write a method to write type: "teacher" if is_teacher is True return object
    def get_type(self):
        if self.is_teacher:
            return "Teacher"
        elif self.is_student:
            return "Student"
        elif self.is_parent:
            return "Parent"
        elif self.is_admin:
            return "Admin"
        return None

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    slug = models.SlugField(max_length=20, unique=True, null=True)
    full_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.full_name} -- {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super(Teacher, self).save(*args, **kwargs)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    slug = models.SlugField(max_length=20, unique=True, null=True)
    full_name = models.CharField(max_length=100, null=True)
    age = models.IntegerField(default=0, null=True)
    group = models.ForeignKey('Group', on_delete=models.SET_NULL, related_name='students', null=True)

    def __str__(self):
        return f"{self.full_name} -- {self.user.username}"
    
    # write a method to get average mark of student in all lessons specified by group
    def get_average_mark(self):
        if hasattr(self, 'marks'):
            average_mark = self.marks.filter(lesson__group=self.group).aggregate(avg_mark=Avg('mark'))
        return average_mark['avg_mark'] or 0

    def save(self, *args, **kwargs):
        if not self.slug or self.user.username != slugify(self.user.username):
            self.slug = slugify(self.user.username)
        super(Student, self).save(*args, **kwargs)


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent')
    slug = models.SlugField(max_length=20, unique=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='parent', null=True)
    full_name = models.CharField(max_length=100, null=True)

    def save(self, *args, **kwargs):
        if not self.slug or self.user.username != slugify(self.user.username):
            self.slug = slugify(self.user.username)
        super(Parent, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} -- {self.user.username}"

    # bu yerda alohida permissionlar yoziladi, hozircha shu oddiy holatda


class StudentProfile(models.Model):
    user = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='student_profile')
    avatar = models.ImageField(upload_to='students/', blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        update save() method by saving profile image setting with and height
        """
        super().save(*args, **kwargs)
        if self.avatar:
            avatar = Image.open(self.avatar.path)
            avatar_width = 300
            avatar_height = 300
            avatar.thumbnail((avatar_width, avatar_height), Image.ANTIALIAS)
            avatar.save(self.avatar.path)

    class Meta:
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'

    def __str__(self):
        return self.user.slug


class TeacherProfile(models.Model):
    user = models.OneToOneField(Teacher, on_delete=models.CASCADE, related_name='teacher_profile')
    avatar = models.ImageField(upload_to='teachers/', blank=True, null=True)

    # write a method to save image with specific width and height
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            avatar = Image.open(self.avatar.path)
            avatar_width = 300
            avatar_height = 300
            avatar.thumbnail((avatar_width, avatar_height), Image.ANTIALIAS)
            avatar.save(self.avatar.path)

    class Meta:
        verbose_name = 'Teacher Profile'
        verbose_name_plural = 'Teacher Profiles'

    def __str__(self):
        return self.user.slug


class Group(models.Model):
    """
    Bu yerda guruhlar yaratiladi va bu Membership orqali kerakli barcha studenlarni
    categoriyga qarab joylaydi
    """

    DAYS = (
        ('Mon, Wed, Fri', 'Mon, Wed, Fri'),
        ('Tue, Thu, Sat', 'Tue, Thu, Sat'),
    )

    name = models.CharField(max_length=150)
    course_date = models.DateField(null=True)
    total_courses = models.IntegerField(default=0, null=True)
    course_time = models.TimeField(null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, related_name='groups', null=True)
    # create a field to get three days of week like Mon, Wed, Fri or Tue, Thu, Sat
    days = models.CharField(max_length=150, choices=DAYS, blank=False, null=True, default='Mon, Wed, Fri')

    def __str__(self):
        return self.name


class Lesson(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='lessons', null=True)
    unite = models.CharField(max_length=150)
    vocabulary = models.CharField(max_length=150)
    grammar = models.CharField(max_length=150)
    home_work = models.CharField(max_length=150)
    date_created = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        if self.group and self.unite:
            return f"{self.group.name} -- {self.unite}"
        elif not self.unite:
            return f"{self.group.name} -- Mavzu yo'q"
        else:
            return f"No group -- nothing to show"

    class Meta:
        ordering = ['-date_created']


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, related_name='attendances')
    come = models.BooleanField(default=False)

    def __str__(self):
        if hasattr(self, 'student') and hasattr(self, 'lesson'):
            return f"{self.student.full_name} -- "
        elif hasattr(self, "student") and not hasattr(self, "lesson"):
            return f"{self.student.full_name} -- No lesson"
        return f"No student -- No lesson"

    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'
        unique_together = ('student', 'lesson')


# create a model to mark students
class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='marks')
    mark = models.IntegerField(default=0, blank=True)

    def __str__(self):
        if hasattr(self, 'student') and hasattr(self, 'lesson'):
            return f"{self.student.full_name} -- {self.lesson.unite} -- {self.mark}"
        elif hasattr(self, "student") and not hasattr(self, "lesson"):
            return f"{self.student.full_name} -- No lesson"
        return f"No student -- No lesson"


    class Meta:
        verbose_name = 'Mark'
        verbose_name_plural = 'Marks'
