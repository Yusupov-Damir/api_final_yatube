from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    """
    Данное ограничение работает в синергии со стандартным IsAuthenticatedOrReadOnly,
    обеспечивая: чтение для всех, ред-е записей только для авторизованных + только для автора
    """
    message = 'Редактирование доступно только авторам.'

    def has_object_permission(self, request, view, obj):
        return (
                request.method in permissions.SAFE_METHODS
                or obj.author == request.user
        )
