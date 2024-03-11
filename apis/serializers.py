from rest_framework import serializers


class AnswerQuestionSerializer(serializers.Serializer):
    answer = serializers.CharField(allow_blank=True, max_length=10000)  # blank for time out

    def validate_answer(self, value):
        if not value:
            raise serializers.ValidationError("Answer is required")
        return value
