from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from core.models import Form, SentForm, TextQuestion, BooleanQuestion, OptionQuestion
from django.utils.timezone import now
from datetime import timedelta

# Vista formulario por form_id y user_id


class TextQuestionSerializer(ModelSerializer):
    class Meta:
        model = TextQuestion
        fields = ['order', 'type', 'text', 'max_chars', 'min_chars', 'is_required']

class BooleanQuestionSerializer(ModelSerializer):
    class Meta:
        model = BooleanQuestion
        fields = ['order', 'type', 'text', 'is_required']

class OptionQuestionSerializer(ModelSerializer):
    class Meta:
        model = OptionQuestion
        fields = ['order', 'type', 'text', 'options', 'is_required']

class SentFormSerializer(ModelSerializer):
    form_name = serializers.CharField(source='form_id.name', read_only=True)
    mesage_end_form = serializers.CharField(source='form_id.message_end_form', read_only=True)
    text_questions = serializers.SerializerMethodField()
    boolean_questions = serializers.SerializerMethodField()
    option_questions = serializers.SerializerMethodField()

    class Meta:
        model = SentForm
        fields = ['id', 'form_id', 'form_name', 'mesage_end_form', 'user_id', 'created', 'sended', 'text_questions', 'boolean_questions', 'option_questions']


    def get_text_questions(self, obj):
        questions = TextQuestion.objects.filter(form_id = obj.form_id)
        return TextQuestionSerializer(questions, many = True).data
    
    def get_boolean_questions(self, obj):
        questions = BooleanQuestion.objects.filter(form_id = obj.form_id)
        return BooleanQuestionSerializer(questions, many = True).data
    
    def get_option_questions(self, obj):
        questions = OptionQuestion.objects.filter(form_id = obj.form_id)
        return OptionQuestionSerializer(questions, many = True).data
    

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