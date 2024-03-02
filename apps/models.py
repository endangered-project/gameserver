from django.db import models

ANSWER_MODE_CHOICES = (
    ('single_right', 'Single (1 right answer, others are wrong)'),
    ('text', 'Text (User input text)')
)

DIFFICULTY_LEVEL_CHOICES = (
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard')
)


class QuestionCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class QuestionModel(models.Model):
    main_class_id = models.IntegerField()
    question = models.TextField()
    answer_property_id = models.IntegerField()
    answer_mode = models.CharField(max_length=100, choices=ANSWER_MODE_CHOICES)
    difficulty_level = models.CharField(max_length=100, choices=DIFFICULTY_LEVEL_CHOICES)
    category = models.ForeignKey(QuestionCategory, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.question

    def get_property_in_question(self):
        property_in_question = self.question.split('{')
        property_in_question = [p.split('}')[0] for p in property_in_question if '}' in p]
        return property_in_question


class GameMode(models.Model):
    name = models.CharField(max_length=100)
    allow_answer_mode = models.CharField(max_length=100, choices=ANSWER_MODE_CHOICES)

    def __str__(self):
        return self.name
