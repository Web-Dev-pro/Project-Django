from rest_framework import serializers
from .models import StudentCommentFromTeacher, CommentReplyToTeacherFromParent

class CommentReplyToTeacherFromParentSerializer(serializers.ModelSerializer):
    parent_data = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = CommentReplyToTeacherFromParent
        fields = (
            'id',
            'comment',
            'parent',
            'reply',
            'parent_data'
        )

    def get_parent_data(self, obj):
        data = {
            "id": obj.parent.id,
            "full name": obj.parent.full_name,
            "username": obj.parent.user.username
        }
        return data
"""
class CommentReplyToTeacherSerializer(serializers.ModelSerializer):
    student_data = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = CommentReplyToTeacher
        fields = (
            'id',
            'comment',
            'student',
            'reply',
            'student_data'
        )

    def get_student_data(self, obj):
        data = {
            "id": obj.student.id,
            "full name": obj.student.full_name,
            "username": obj.student.user.username
        }
        return data
"""

class StudentCommentFromTeacherSerializer(serializers.ModelSerializer):
    # comment_reply = CommentReplyToTeacherSerializer(many=True, read_only=True)
    comment_reply_from_parent = CommentReplyToTeacherFromParentSerializer(many=True, read_only=True)
    teacher_data = serializers.SerializerMethodField(read_only=True)
    student_data = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = StudentCommentFromTeacher
        fields = (
            'id',
            'student',
            'student_data',
            'lesson',
            'teacher',
            'teacher_data',
            'comment',
            'comment_reply_from_parent',
        )

    def get_student_data(self, obj):
        data = {
            "id": obj.student.id,
            "full name": obj.student.full_name,
            "username": obj.student.user.username
        }
        return data
    
    def get_teacher_data(self, obj):
        data = {
            "id": obj.teacher.id,
            "full name": obj.teacher.full_name,
            "username": obj.teacher.user.username
        }
        return data