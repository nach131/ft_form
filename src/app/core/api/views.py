from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from django.utils.timezone import now
from core.models import SentForm
from .serializers import SentFormSerializer, UserFormsSerializer
from .permissions import IsUserOfSentForm

class SentFormView(APIView):
    # permission_classe = [IsAuthenticated]

    def get(self, request, user_id, sent_form_id):
        # Asegura que el usuario se ha autenticado y el formulario va dirigido a el
        # if request.user.id != user_id:
        #     raise PermissionDenied("No tienes acceso a este formulario")
        try:
            sent_form = SentForm.objects.get(id= sent_form_id, user_id=user_id)
        except SentForm.DoesNotExist:
            return Response(
                {"detail": "Formulario no encontrado"},
                 status=status.HTTP_404_NOT_FOUND,
            )
        if now() < sent_form.sended:
            return Response(
                {"detail": "El formulario aún no está disponible"},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = SentFormSerializer(sent_form)
        return Response(serializer.data)
    
class   FormsByUserView(APIView):
    # permission_classe = [IsAuthenticated]

    def get(self, request, user_id):
        # Asegura que el usuario se ha autenticado y estos formularios van dirigidos a el
        # if request.user.id != user_id:
        #     raise PermissionDenied("No tienes acceso a estos formularios")
        try:
            user_forms   = SentForm.objects.filter(user_id=user_id, sended__lte=now())
        except SentForm.DoesNotExist:
            return Response(
                {"detail": "Formularios no encontrados"},
                 status=status.HTTP_404_NOT_FOUND,
            )
        serializer = UserFormsSerializer(user_forms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)