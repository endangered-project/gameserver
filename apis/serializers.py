from rest_framework import serializers


class AnswerQuestionSerializer(serializers.Serializer):
    answer = serializers.CharField(allow_blank=True, max_length=10000)  # blank for time out
    duration = serializers.FloatField(default=0.0)
