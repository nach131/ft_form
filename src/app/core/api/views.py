from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from django.utils.timezone import now
from core.models import (SentForm, TextQuestion, BooleanQuestion, OptionQuestion, MultipleChoiceQuestion,
                         NumberQuestion, EmailQuestion, ScaleQuestion, DateQuestion, URLQuestion, FileQuestion)
from core.models import (Answer, CharFieldAnswer, BooleanAswer, SingleChoiceAnswer, MultipleChoiceAnswer, NumberAnswer,
                         EmailAnswer, ScaleAnswer,DateAnswer, URLAnswer, FileAnswer)
from .serializers import SentFormSerializer, UserFormsSerializer
from .permissions import IsUserOfSentForm


# Vista de un SentForm especifico defindo por sent_form_id de un usuario especifico definido por user_id
class SentFormView(APIView):
    permission_classe = [IsAuthenticated]

    # Este metodo get obtiene la informacion del formulario y las preguntas relacionadas con el
    #de esta manera envía esa informacion al endpoint
    def get(self, request, user_id, sent_form_id):
        # Asegura que el usuario se ha autenticado y el formulario va dirigido a el
        if request.user.id != user_id:
            raise PermissionDenied("No tienes acceso a este formulario")
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
    
    # Este método va a tomar las respuestas del alumno y registrarlas, actualizando en la BBDD
    # los valores de SentForm, creando un registro de Answer cuyo sent_form_id sea igual al 
    #sent_form_id enviado y creara tambien un registro de respuesta cuyo tipo (CharFielAnswer, BooleanAnswer o
    # SingleChoiceAnswer) dependera de el tipo de pregunta enviada
    def post(self, request, user_id, sent_form_id):

        # Primero validamos que el SentForm existe y pertenece al usuario
        try:
            sent_form = SentForm.objects.get(id=sent_form_id, user_id=user_id)
        except SentForm.DoesNotExist:
            return Response({"detail":"Formulario no encontrado"},
                status=status.HTTP_404_NOT_FOUND,)
        
        # Ahora validamos que el SentForm no haya sido respondido ya
        if sent_form.answered:
            return Response({"detail":"El formulario ya ha sido respondido"},
                status=status.HTTP_400_BAD_REQUEST)
    
        # Ahora valdamos que el formulario ya esté disponible, es decir, que el valor
        # de sent_form.sended sea menor que la fecha actual
        if now() < sent_form.sended:
            return Response({"detail": "El formulario aún no está disponible"},
                status=status.HTTP_403_FORBIDDEN)

        # Extraemos las respuestas del cuerpo de la solicitud
        responses = request.data.get("responses", [])
        # Si no hay respuestas, lanzamos un error
        if not responses:
            return Response({"detail": "No se enviaron las respuestas"},
                status=status.HTTP_400_BAD_REQUEST,)

        # Creamos un registro de Answer
        answer = Answer.objects.create(
            user_id = user_id,
            sent_form_id = sent_form.id,
            created_at = now(),
        )

        # Procesamos cada tipo de pregunta y creamos un registro de respuesta
        #acorde al tipo de pregunta
        for response in responses:
            question_type = response.get("question_type")
            question_id = response.get("question_id")
            value = response.get("value")

            if question_type == "text":
                # Validamos que esa pregunta exista, es decir, que el question_id
                #que se envía realmente exista en nuestra BBDD
                try:
                    question = TextQuestion.objects.get(id=question_id)
                except TextQuestion.DoesNotExist:
                    return Response({"detail": f"Pregunta de texto con id {question_id} no encontrada"},
                        status=status.HTTP_404_NOT_FOUND,)
                # Ahora creamos el registro de CharFieldAnswer
                CharFieldAnswer.objects.create(
                    value = value,
                    answer_id = answer,
                    question_id = question,
                )

            elif question_type == "boolean":
                # Validamos que esa pregunta exista, es decir, que el question_id
                #que se envía realmente exista en nuestra BBDD
                try:
                    question = BooleanQuestion.objects.get(id=question_id)
                except BooleanQuestion.DoesNotExist:
                    return Response({"detail": f"Pregunta booleana con id {question_id} no encontrada"},
                        status=status.HTTP_404_NOT_FOUND,)
                # Ahora creamos el registro de BooleanAnswer
                BooleanAswer.objects.create(
                    value = value,
                    answer_id = answer,
                    question_id = question,
                )

            elif question_type == "option":
                # Validamos que esa pregunta exista, es decir, que el question_id
                #que se envía realmente exista en nuestra BBDD
                try:
                    question = OptionQuestion.objects.get(id=question_id)
                except OptionQuestion.DoesNotExist:
                    return Response({"detail": f"Pregunta opciones con id {question_id} no encontrada"},
                        status=status.HTTP_404_NOT_FOUND,)
                # Ahora creamos el registro de SingleChoiceAnswer
                SingleChoiceAnswer.objects.create(
                    value = value,
                    answer_id = answer,
                    question_id = question,
                )
            elif question_type == "multiple_choice":
                # Validamos que esa pregunta exista, es decir, que el question_id
                #que se envía realmente exista en nuestra BBDD
                try:
                    question = MultipleChoiceQuestion.objects.get(id=question_id)
                except MultipleChoiceQuestion.DoesNotExist:
                    return Response({"detail": f"Pregunta multi opciones con id {question_id} no encontrada"},
                        status=status.HTTP_404_NOT_FOUND,)
                # Ahora creamos el registro de MultipleChoiceAnswer
                MultipleChoiceAnswer.objects.create(
                    value = value,
                    answer_id = answer,
                    question_id = question,
                )

            elif question_type == "number":
                # Validamos que esa pregunta exista, es decir, que el question_id
                #que se envía realmente exista en nuestra BBDD
                try:
                    question =NumberQuestion.objects.get(id=question_id)
                except NumberQuestion.DoesNotExist:
                    return Response({"detail": f"Pregunta number con id {question_id} no encontrada"},
                        status=status.HTTP_404_NOT_FOUND,)
                # Ahora creamos el registro de NumberAnswer
                NumberAnswer.objects.create(
                    value = value,
                    answer_id = answer,
                    question_id = question,
                )

            elif question_type == "email":
                # Validamos que esa pregunta exista, es decir, que el question_id
                #que se envía realmente exista en nuestra BBDD
                try:
                    question =EmailQuestion.objects.get(id=question_id)
                except EmailQuestion.DoesNotExist:
                    return Response({"detail": f"Pregunta email con id {question_id} no encontrada"},
                        status=status.HTTP_404_NOT_FOUND,)
                # Ahora creamos el registro de EmailAnswer
                EmailAnswer.objects.create(
                    value = value,
                    answer_id = answer,
                    question_id = question,
                )

            elif question_type == "scale":
                # Validamos que esa pregunta exista, es decir, que el question_id
                #que se envía realmente exista en nuestra BBDD
                try:
                    question =ScaleQuestion.objects.get(id=question_id)
                except ScaleQuestion.DoesNotExist:
                    return Response({"detail": f"Pregunta scale con id {question_id} no encontrada"},
                        status=status.HTTP_404_NOT_FOUND,)
                # Ahora creamos el registro de ScaleAnswer
                ScaleAnswer.objects.create(
                    value = value,
                    answer_id = answer,
                    question_id = question,
                )

            elif question_type == "date":
                # Validamos que esa pregunta exista, es decir, que el question_id
                #que se envía realmente exista en nuestra BBDD
                try:
                    question =DateQuestion.objects.get(id=question_id)
                except DateQuestion.DoesNotExist:
                    return Response({"detail": f"Pregunta date con id {question_id} no encontrada"},
                        status=status.HTTP_404_NOT_FOUND,)
                # Ahora creamos el registro de DateAnswer
                DateAnswer.objects.create(
                    value = value,
                    answer_id = answer,
                    question_id = question,
                )

            elif question_type == "url":
                # Validamos que esa pregunta exista, es decir, que el question_id
                #que se envía realmente exista en nuestra BBDD
                try:
                    question =URLQuestion.objects.get(id=question_id)
                except URLQuestion.DoesNotExist:
                    return Response({"detail": f"Pregunta url con id {question_id} no encontrada"},
                        status=status.HTTP_404_NOT_FOUND,)
                # Ahora creamos el registro de URLAnswer
                URLAnswer.objects.create(
                    value = value,
                    answer_id = answer,
                    question_id = question,
                )

            elif question_type == "file":
                # Validamos que esa pregunta exista, es decir, que el question_id
                #que se envía realmente exista en nuestra BBDD
                try:
                    question =FileQuestion.objects.get(id=question_id)
                except FileQuestion.DoesNotExist:
                    return Response({"detail": f"Pregunta file con id {question_id} no encontrada"},
                        status=status.HTTP_404_NOT_FOUND,)
                # Ahora creamos el registro de FileAnswer
                FileAnswer.objects.create(
                    value = value,
                    answer_id = answer,
                    question_id = question,
                )

            else:
                return Response({"detail": f"Tipo de pregunta desconocido: {question_type}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
        # Cambiamos el valor de SentForm.answered a True
        sent_form.answered = True
        sent_form.save()

        # Actualizamos el valor de answer.is_valid a true
        answer.is_valid = True
        answer.save()

        return Response({"detail": "Respuestas guardadas correctamente"},
                    status=status.HTTP_201_CREATED,)



class   FormsByUserView(APIView):
    permission_classe = [IsAuthenticated]

    def get(self, request, user_id):
        # Asegura que el usuario se ha autenticado y estos formularios van dirigidos a el
        if request.user.id != user_id:
            raise PermissionDenied("No tienes acceso a estos formularios")
        try:
            user_forms   = SentForm.objects.filter(user_id=user_id, sended__lte=now())
        except SentForm.DoesNotExist:
            return Response(
                {"detail": "Formularios no encontrados"},
                 status=status.HTTP_404_NOT_FOUND,
            )
        serializer = UserFormsSerializer(user_forms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)