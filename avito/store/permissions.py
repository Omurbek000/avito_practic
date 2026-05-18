from rest_framework.permissions import BasePermission

class IsProductOwner(BasePermission):
    """
    Object-level permission – только владелец товара может его изменять.
    """
    def has_object_permission(self, request, view, obj):
        # obj – это экземпляр Product
        return obj.owner == request.user