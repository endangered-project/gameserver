from django.contrib.auth.models import User
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


class UserCategoryWeight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE)
    weight = models.FloatField(default=0.0)

    def __str__(self):
        return self.user.username + ' - ' + self.category.name + '(' + str(self.weight) + ')'


class TextCustomQuestion(models.Model):
    question = models.TextField()
    choices = models.TextField()
    answer = models.TextField()
    difficulty_level = models.CharField(max_length=100, choices=DIFFICULTY_LEVEL_CHOICES)
    category = models.ForeignKey(QuestionCategory, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.question


class ImageCustomQuestion(models.Model):
    question = models.TextField()
    choices = models.TextField()
    answer = models.TextField()
    difficulty_level = models.CharField(max_length=100, choices=DIFFICULTY_LEVEL_CHOICES)
    category = models.ForeignKey(QuestionCategory, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.question


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    score = models.IntegerField(default=0)
    # weight will store in {category_id: weight} format
    weight = models.JSONField(default=dict)
    finished = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + ' - ' + str(self.start_time)

    def has_lose(self):
        print(GameQuestion.objects.filter(game=self, is_true=False, answered=True).count())
        if GameQuestion.objects.filter(game=self, is_true=False, answered=True).count() >= 3:
            return True
        return False


class QuestionHistory(models.Model):
    question_mode = models.CharField(max_length=100)
    category = models.ForeignKey(QuestionCategory, on_delete=models.SET_NULL, null=True)
    difficulty_level = models.CharField(max_length=100, choices=DIFFICULTY_LEVEL_CHOICES)
    question = models.TextField(blank=True, null=True)
    choice = models.TextField(blank=True, null=True)
    answer = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=100)
    full_json = models.JSONField(default=dict)

    def __str__(self):
        return self.question + ' - ' + self.question_mode + ' - ' + self.type

    def get_right_weight(self):
        if self.difficulty_level == 'easy':
            return 0.5
        elif self.difficulty_level == 'medium':
            return 1
        else:
            return 2

    def get_wrong_weight(self):
        if self.difficulty_level == 'easy':
            return -0.25
        elif self.difficulty_level == 'medium':
            return -0.5
        else:
            return 1


class GameQuestion(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionHistory, on_delete=models.CASCADE)
    game_mode = models.ForeignKey(GameMode, on_delete=models.CASCADE)
    is_true = models.BooleanField(default=False)
    answered = models.BooleanField(default=False)

    def __str__(self):
        return self.game.user.username + ' - ' + self.question.question + ' - ' + self.game_mode.name

    def get_weight(self):
        if self.is_true:
            return self.question.get_right_weight()
        else:
            return self.question.get_wrong_weight()

    def get_score(self):
        if self.is_true:
            if self.question.difficulty_level == 'easy':
                return 50
            elif self.question.difficulty_level == 'medium':
                return 100
            else:
                return 200
        return 0
