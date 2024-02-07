from django.db import models


class QuestionModel(models.Model):
    main_class_id = models.IntegerField()
    question = models.TextField()
    answer_property_id = models.IntegerField()

    def __str__(self):
        return self.question


class GameMode(models.Model):
    name = models.CharField(max_length=100)
    answer_mode = models.CharField(max_length=100)

    def __str__(self):
        return self.name
