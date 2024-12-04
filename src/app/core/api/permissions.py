from rest_framework.permissions import BasePermission


class   IsUserOfSentForm(BasePermission):
    # Permiso para verificar que el alumnoi identificado es el asignado al formulario
    def has_form_permission(self, request, view, obj):
        return obj.user_id.id == request.user.id