# import permissions from rest_framework
from rest_framework import permissions

class CurrentUserIsTeacher(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_teacher or request.user.is_admin:
            return True
    
class CurrentUserIsStudent(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_student
    
class CurrentUserIsParent(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_parent