from django.db import models

from apps.authentication.models import (
    User,
    Student,
    Lesson,
    Teacher,
    Parent
)
from django.template.defaultfilters import truncatechars


class StudentCommentFromTeacher(models.Model):
    """
    1. Har bir student, Lesson, Teacher o'chirib yuborilagda comment ham o'chib ketadi
    2. Yoki Comment saqlanib qolishi uchun ko'd o'zgartiriladi, NULL bo'ladi
    Variant ko'rib chiqiladi
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_comment')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_comment')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_comment')
    comment = models.TextField()

    def __str__(self):
        return f'{self.student} -- {self.lesson} -- {self.teacher} -- {self.comment}'

    def get_comment_as_truncated(self):
        return truncatechars(self.comment, 20)

    class Meta:
        verbose_name = 'Student Comment From Teacher'
        verbose_name_plural = 'Student Comments From Teachers'
        ordering = ['-id']
"""
class CommentReplyToTeacher(models.Model):
    comment = models.ForeignKey(StudentCommentFromTeacher, on_delete=models.CASCADE, related_name='comment_reply')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_reply')
    reply = models.TextField()

    def __str__(self):
        return f'{self.comment} -- {self.student} -- {self.reply}'

    def get_reply_as_truncated(self):
        return truncatechars(self.reply, 20)

    class Meta:
        verbose_name = 'Comment Reply To Teacher'
        verbose_name_plural = 'Comment Replies To Teachers'
        ordering = ['-id']
"""

class CommentReplyToTeacherFromParent(models.Model):
    comment = models.ForeignKey(StudentCommentFromTeacher, on_delete=models.CASCADE, related_name='comment_reply_from_parent')
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='parent_reply')
    reply = models.TextField()

    def __str__(self):
        return f'{self.comment} -- {self.parent.user.username} -- {self.reply}'

    def get_reply_as_truncated(self):
        """
        make reply text short as 20 max length word
        """
        return truncatechars(self.reply, 20)

    class Meta:
        verbose_name = 'Comment Reply To Teacher From Parent'
        verbose_name_plural = 'Comment Replies To Teachers From Parents'
        ordering = ['-id']