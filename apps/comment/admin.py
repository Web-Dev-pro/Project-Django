from django.contrib import admin

from .models import StudentCommentFromTeacher, CommentReplyToTeacherFromParent


class CustomCommentAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'teacher', 'get_comment_as_truncated')
    search_fields = ('student', 'lesson', 'teacher', 'comment')
    list_filter = ('student', 'lesson', 'teacher', 'comment')

class CustomReplyFromParentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'parent', 'get_reply_as_truncated')
    search_fields = ('comment', 'parent', 'reply')
    list_filter = ('comment', 'parent', 'reply')

admin.site.register(StudentCommentFromTeacher, CustomCommentAdmin)
admin.site.register(CommentReplyToTeacherFromParent, CustomReplyFromParentAdmin)