from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from core.models import SentForm, TextQuestion, BooleanQuestion, OptionQuestion

class TextQuestionSerializer(ModelSerializer):
    class Meta:
        model = TextQuestion
        fields = ['order', 'type', 'text']

class BooleanQuestionSerializer(ModelSerializer):
    class Meta:
        model = BooleanQuestion
        fields = ['order', 'type', 'text']

class OptionQuestionSerializer(ModelSerializer):
    class Meta:
        model = OptionQuestion
        fields = ['order', 'type', 'text', 'options']

class SentFormSerializer(ModelSerializer):
    text_questions = serializers.SerializerMethodField()
    boolean_questions = serializers.SerializerMethodField()
    option_questions = serializers.SerializerMethodField()

    class Meta:
        model = SentForm
        fields = ['id', 'form_id', 'user_id', 'created', 'sended', 'text_questions', 'boolean_questions', 'option_questions']

    def get_text_question(self, obj):
        questions = TextQuestion.objects.filter(form_id = obj.form_id)
        return TextQuestionSerializer(questions, many = True).data
    
    def get_boolean_question(self, obj):
        questions = TextQuestion.objects.filter(form_id = obj.form_id)
        return TextQuestionSerializer(questions, many = True).data
    
    def get_option_question(self, obj):
        questions = TextQuestion.objects.filter(form_id = obj.form_id)
        return TextQuestionSerializer(questions, many = True).data