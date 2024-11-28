from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from core.models import SentForm
from .serializers import SentFormSerializer

class SentFormView(APIView):
    def get(self, request, user_id, sent_form_id):
        try:
            sent_form = SentForm.objects.get(id= sent_form_id, user_id=user_id)
        except SentForm.DoesNotExist:
            raise NotFound("Este formulario no existe para este usuario")
        serializer = SentFormSerializer(sent_form)
        return Response(serializer.data)