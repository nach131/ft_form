from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from core.models import (Form, SentForm, TextQuestion, BooleanQuestion,
                        OptionQuestion, MultipleChoiceQuestion, NumberQuestion,
                        EmailQuestion, ScaleQuestion,
                        DateQuestion, URLQuestion, FileQuestion)
from django.utils.timezone import now
from datetime import timedelta

# Vista formulario por form_id y user_id


class TextQuestionSerializer(ModelSerializer):
    class Meta:
        model = TextQuestion
        fields = ['id', 'order', 'type', 'text', 'max_chars', 'min_chars', 'is_required']

class BooleanQuestionSerializer(ModelSerializer):
    class Meta:
        model = BooleanQuestion
        fields = ['id', 'order', 'type', 'text', 'is_required']

class OptionQuestionSerializer(ModelSerializer):
    class Meta:
        model = OptionQuestion
        fields = ['id', 'order', 'type', 'text', 'options', 'is_required']

class MultipleChoiceQuestionSerializer(ModelSerializer):
    class Meta:
        model = MultipleChoiceQuestion
        fields = ['id', 'order', 'type', 'text', 'options', 'is_required']

class NumberQuestionSerializer(ModelSerializer):
    class Meta:
        model = NumberQuestion
        fields = ['id', 'order', 'type', 'text', 'is_required']

class EmailQuestionSerializer(ModelSerializer):
	class Meta:
		model = EmailQuestion
		fields = ['id', 'order', 'type', 'text', 'is_required']

class ScaleQuestionSerializer(ModelSerializer):
	class Meta:
		model = ScaleQuestion
		fields = ['id', 'order', 'type', 'text', 'min_value', 'max_value', 'is_required']

class DateQuestionSerializer(ModelSerializer):
    class Meta:
        model = DateQuestion
        fields = ['id', 'order', 'type', 'text', 'is_required']
        
class URLQuestionSerializer(ModelSerializer):
    class Meta:
        model = URLQuestion
        fields = ['id', 'order', 'type', 'text', 'is_required']

class FileQuestionSerializer(ModelSerializer):
    class Meta:
        model = FileQuestion
        fields = ['id', 'order', 'type', 'text', 'is_required']

# class SentFormSerializer(ModelSerializer):
#     form_name = serializers.CharField(source='form_id.name', read_only=True)
#     mesage_end_form = serializers.CharField(source='form_id.message_end_form', read_only=True)
#     text_questions = serializers.SerializerMethodField()
#     boolean_questions = serializers.SerializerMethodField()
#     option_questions = serializers.SerializerMethodField()

#     class Meta:
#         model = SentForm
#         fields = ['id', 'form_id', 'form_name', 'mesage_end_form', 'user_id', 'created', 'sended', 'text_questions', 'boolean_questions', 'option_questions']


#     def get_text_questions(self, obj):
#         questions = TextQuestion.objects.filter(form_id = obj.form_id)
#         return TextQuestionSerializer(questions, many = True).data
    
#     def get_boolean_questions(self, obj):
#         questions = BooleanQuestion.objects.filter(form_id = obj.form_id)
#         return BooleanQuestionSerializer(questions, many = True).data
    
#     def get_option_questions(self, obj):
#         questions = OptionQuestion.objects.filter(form_id = obj.form_id)
#         return OptionQuestionSerializer(questions, many = True).data
    

class SentFormSerializer(ModelSerializer):
    form_name = serializers.CharField(source='form_id.name', read_only=True)
    mesage_end_form = serializers.CharField(source='form_id.message_end_form', read_only=True)
    questions = serializers.SerializerMethodField()

    class Meta:
        model = SentForm
        fields = ['id', 'form_id', 'form_name', 'mesage_end_form', 'user_id', 'created', 'sended', 'questions']

    def get_questions(self, obj):
        """
        Agrupa todas las preguntas relacionadas con el formulario en una lista.
        Cada entrada incluye el tipo de pregunta y los detalles específicos.
        """
        # Obtén todas las preguntas relacionadas
        text_questions = TextQuestion.objects.filter(form_id=obj.form_id)
        boolean_questions = BooleanQuestion.objects.filter(form_id=obj.form_id)
        option_questions = OptionQuestion.objects.filter(form_id=obj.form_id)
        multiple_choice_questions = MultipleChoiceQuestion.objects.filter(form_id=obj.form_id)
        number_questions = NumberQuestion.objects.filter(form_id=obj.form_id)
        email_questions = EmailQuestion.objects.filter(form_id=obj.form_id)
        scale_questions = ScaleQuestion.objects.filter(form_id=obj.form_id)
        date_questions = DateQuestion.objects.filter(form_id=obj.form_id)
        url_questions = URLQuestion.objects.filter(form_id=obj.form_id)
        file_questions = FileQuestion.objects.filter(form_id=obj.form_id)

        # Serializa las preguntas y agrega un campo `type` explícito
        questions = []

        for question in text_questions:
            serialized = TextQuestionSerializer(question).data
            serialized['type'] = 'text'
            questions.append(serialized)

        for question in boolean_questions:
            serialized = BooleanQuestionSerializer(question).data
            serialized['type'] = 'boolean'
            questions.append(serialized)

        for question in option_questions:
            serialized = OptionQuestionSerializer(question).data
            serialized['type'] = 'option'
            questions.append(serialized)

        for question in multiple_choice_questions:
            serialized = MultipleChoiceQuestionSerializer(question).data
            serialized['type'] = 'multiple_choice'
            questions.append(serialized)

        for question in number_questions:
            serialized = NumberQuestionSerializer(question).data
            serialized['type'] = 'number'
            questions.append(serialized)

        for question in email_questions:
            serialized = EmailQuestionSerializer(question).data
            serialized['type'] = 'email'
            questions.append(serialized)

        for question in scale_questions:
            serialized = ScaleQuestionSerializer(question).data
            serialized['type'] = 'scale'
            questions.append(serialized)
        
        for question in date_questions:
            serialized = DateQuestionSerializer(question).data
            serialized['type'] = 'date'
            questions.append(serialized)
            
        for question in url_questions:
            serialized = URLQuestionSerializer(question).data
            serialized['type'] = 'url'
            questions.append(serialized)
            
        for question in file_questions:
            serialized = FileQuestionSerializer(question).data
            serialized['type'] = 'file'
            questions.append(serialized)

        return questions


# Vista de los formularios por user_id

class   FormSerializer(ModelSerializer):
    class Meta:
        model = Form
        fields = ['name', 'message_end_form']

class   UserFormsSerializer(ModelSerializer):
    form_details = FormSerializer(source='form_id', read_only=True)
    is_new = serializers.SerializerMethodField()

    class Meta:
        model = SentForm
        fields = ['id', 'form_id', 'form_details', 'user_id', 'sended', 'is_new']

    def get_is_new(self, obj):
        five_days_ago = now() - timedelta(days=5)
        return obj.sended > five_days_ago