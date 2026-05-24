from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsProductOwner(BasePermission):
    """
    Разрешение — только владелец товара может его редактировать или удалять.

    Логика:
    - GET, HEAD, OPTIONS (SAFE_METHODS) — разрешено всем
    - POST, PUT, PATCH, DELETE — только владелец объекта (obj.owner == request.user)

    Использование во view:
        permission_classes = [IsAuthenticated, IsProductOwner]
    """

    def has_permission(self, request, view):
        # Базовая проверка — пользователь должен быть авторизован
        # для любых изменяющих запросов
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Чтение разрешено всем
        if request.method in SAFE_METHODS:
            return True

        # Запись — только владелец товара
        return obj.owner == request.user


class IsOwnerOrReadOnly(BasePermission):
    """
    Универсальное разрешение — только владелец объекта может его изменять.
    Подходит для любой модели у которой есть поле user или owner.

    Использование во view:
        permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    """

    def has_object_permission(self, request, view, obj):
        # Чтение разрешено всем
        if request.method in SAFE_METHODS:
            return True

        # Проверяем поле owner (для Product) или user (для Review и др.)
        if hasattr(obj, "owner"):
            return obj.owner == request.user
        if hasattr(obj, "user"):
            return obj.user == request.user

        return False
