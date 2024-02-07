from django.db import models


class QuestionModel(models.Model):
    main_class_id = models.IntegerField()
    question = models.TextField()
    answer_property_id = models.IntegerField()

    def __str__(self):
        return self.question

    def get_property_in_question(self):
        property_in_question = self.question.split('{')
        property_in_question = [p.split('}')[0] for p in property_in_question if '}' in p]
        return property_in_question


class GameMode(models.Model):
    name = models.CharField(max_length=100)
    answer_mode = models.CharField(max_length=100)

    def __str__(self):
        return self.name
