from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Faqat ob'ekt egalariga uni tahrirlashiga ruxsat berish uchun maxsus ruxsat.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user
