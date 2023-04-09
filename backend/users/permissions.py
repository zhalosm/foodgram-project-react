from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    """
    Класс разрешающее редактировать объект только авторам.
    """
    def has_permission(self, request, view):
        """
        Возвращает True, если метод запроса безопасен
        или пользователь аутентифицирован.
        """
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """
        Возвратите True, если метод запроса безопасен
        или аутентифицированный пользователь является автором объекта.
        """
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
