from rest_framework import permissions

class IsprofileOwner(permissions.BasePermission):
     def has_permission(self, request, view):
        # Permite GET, PUT, PATCH solo a usuarios autenticados
        return request.user.is_authenticated

     def has_object_permission(self, request, view, obj):
        # Verifica que el usuario sea dueño del perfil
        return obj.id == request.user.id