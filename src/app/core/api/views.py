from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from core.models import SentForm
from .serializers import SentFormSerializer
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
            raise NotFound("Este formulario no existe para este usuario")
        serializer = SentFormSerializer(sent_form)
        return Response(serializer.data)