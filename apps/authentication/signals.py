import logging

from django.db import IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (
    Student,
    Teacher,
    Group,
    Lesson,
    Parent,
    # profile qism uchun
    StudentProfile,
    TeacherProfile,
    Attendance,
    Mark
)

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Student)
def create_and_save_student_profile(sender, instance, created, **kwargs):
    """
    Student model yaratilganda StudentProfile modelni ham yaratadi
    """
    if created:
        try:
            StudentProfile.objects.create(user=instance)
            print("Student profile created successfully")
        except Exception as e:
            logger.error(f"Error while creating student profile: {e}")
            print(f"Error while creating student profile: {e}")
        else:
            logger.debug(f"Student profile created successfully")


@receiver(post_save, sender=Teacher)
def create_and_save_teacher_profile(sender, instance, created, **kwargs):
    """
    Teacher model yaratilganda TeacherProfile modelni ham yaratadi
    """
    if created:
        try:
            TeacherProfile.objects.create(user=instance)
        except Exception as e:
            logger.error(f"Error while creating Teacher profile: {e}")
        else:
            logger.debug(f"Teacher profile created successfully")

# @receiver(post_save, sender=Student)
# def create_and_save_lesson_by_attendance(sender, instance, created, **kwargs):
#     if created and instance.group:
#         if instance.group.lessons.count() == 0:
#             try:
#                 lesson = Lesson.objects.create(group=instance.group)
#                 Attendance.objects.create(student=instance, lesson=lesson)
#                 Mark.objects.create(student=instance, lesson=lesson)
#             except IntegrityError as e:
#                 logger.error(f"Error while creating Lesson, Attendance and Marks: {e}")
#             except Exception as e:
#                 logger.error(f"Unhandled error happened: {e}")
#             else:
#                 logger.info(f"Lesson created successfully")
#         else:
#             logger.info("Groupda lesson bor. Lesson yaratilmadi")
#             try:
#                 lesson = instance.group.lessons.first()
#                 Attendance.objects.create(student=instance, lesson=lesson)
#                 Mark.objects.create(student=instance, lesson=lesson)
#             except Exception as e:
#                 logger.error(f"Error while creating Attendance and Mark: {e}")
#             else:
#                 logger.info(f"Attendance and Mark created successfully")
#     else:
#         logger.debug("Gruppada studentlar topilmadi. Attendance va Mark yaratilmadi")


@receiver(post_save, sender=Lesson)
def auto_create_attendance_and_lesson(sender, instance, created, **kwargs):

    if created:
        try:
            students = instance.group.students.filter(group=instance.group)
            for student in students:
                Attendance.objects.create(student=student, lesson=instance)
                Mark.objects.create(student=student, lesson=instance)
        except IntegrityError as e:
            logger.error(f"Error while creating Attendance and Mark: {e}")
        except ValueError as e:
            logger.error(f"Unhandled error while createing Attendance and Mark: {e}")
        else:
            logger.info(f"Attendance and Mark created successfully")
    else:
        logger.debug("Groupda studentlar topilmadi. Attendance va Mark yaratilmadi")
    
        
