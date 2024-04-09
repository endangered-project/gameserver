import json

from django import forms
from django.core.validators import FileExtensionValidator

from apps.models import QuestionModel, ANSWER_MODE_CHOICES, QuestionCategory, TextCustomQuestion
from apps.seed_api import get_all_class, get_property_type_from_class


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class QuestionModelForm(forms.Form):
    main_class_id = forms.CharField(
        label='Main Class',
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
        help_text='The class within the knowledge base that will be used for this question.'
    )
    question = forms.CharField(
        label='Question',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        ),
        max_length=1000,
        help_text='The question text that will be shown. Must include {property_name} to act as the question property.'
    )
    answer_property_id = forms.CharField(
        label='Answer Property',
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
        help_text='The property that will be used as the answer to this question.'
    )
    answer_mode = forms.CharField(
        label='Answer Mode',
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            },
            choices=ANSWER_MODE_CHOICES
        ),
        help_text='This defines how the user must answer the question.',
        required=True
    )
    difficulty_level = forms.CharField(
        label='Difficulty Level',
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            },
            choices=[
                ('easy', 'Easy'),
                ('medium', 'Medium'),
                ('hard', 'Hard')
            ]
        ),
        help_text='The difficulty of the question compared to others in the same category. This affects the question is selected based on a user\'s category score.',
        required=True
    )
    category = forms.ModelChoiceField(
        label='Category',
        queryset=QuestionCategory.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
        help_text='The category of the question.'
    )

    class Meta:
        model = QuestionModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(QuestionModelForm, self).__init__(*args, **kwargs)
        if 'category' not in self.initial:
            try:
                self.initial['category'] = QuestionCategory.objects.get(name='Uncategorized')
            except QuestionCategory.DoesNotExist:
                pass

    def clean(self):
        cleaned_data = super().clean()
        main_class_id = cleaned_data.get('main_class_id')
        question = cleaned_data.get('question')
        answer_property_id = cleaned_data.get('answer_property_id')
        all_class = get_all_class()
        # check main class exist
        class_id_list = [str(c['id']) for c in all_class]
        if main_class_id not in class_id_list:
            self.add_error('main_class_id', 'Main class is not exist')
        # check all property in question (use {property_name}) exist
        all_property = get_property_type_from_class(main_class_id)
        all_property_name = [p['name'] for p in all_property]
        all_property_id = [str(p['id']) for p in all_property]
        all_property_in_question = question.split('{')
        all_property_in_question = [p.split('}')[0] for p in all_property_in_question if '}' in p]
        for p in all_property_in_question:
            if p not in all_property_name:
                self.add_error('question', f'Property {p} does not exist in main class')
        # check answer property exist
        print(all_property_name)
        if answer_property_id not in all_property_id:
            self.add_error('answer_property_id', 'Answer property does not exist')


class GameModeForm(forms.Form):
    name = forms.CharField(
        label='Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
        help_text='The name of game mode.',
        required=True
    )
    allow_answer_mode = forms.CharField(
        label='Allow Answer Mode',
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            },
            choices=ANSWER_MODE_CHOICES
        ),
        help_text='How the game mode is answered.',
        required=True
    )

    class Meta:
        model = QuestionModel
        fields = '__all__'


class QuestionCategoryForm(forms.ModelForm):
    name = forms.CharField(
        label='Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
        help_text='The name of the category.'
    )
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        ),
        help_text='The description of the category.',
        required=False
    )

    class Meta:
        model = QuestionCategory
        fields = '__all__'


class TextCustomQuestionForm(forms.Form):
    question = forms.CharField(
        label='Question',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        ),
        help_text='The question text of this custom question.'
    )
    choices = forms.CharField(
        label='Choices',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        ),
        help_text='The available choices in JSON list format. For example: ["choice1", "choice2", "choice3", "choice4"]. A minimum of 4 choices are needed.'
    )
    answer = forms.CharField(
        label='Answer',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
        help_text='The answer in JSON list format. For example: ["choice1"]. It must exist in the choices and the difference between correct and incorrect answers must be of at least 3.'
    )
    difficulty_level = forms.CharField(
        label='Difficulty Level',
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            },
            choices=[
                ('easy', 'Easy'),
                ('medium', 'Medium'),
                ('hard', 'Hard')
            ]
        ),
        help_text='The difficulty of the question compared to others in the same category. This affects the question is selected based on a user\'s category score.'
    )
    category = forms.ModelChoiceField(
        label='Category',
        queryset=QuestionCategory.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
        help_text='The category of this custom question.'
    )

    class Meta:
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'category' not in self.initial:
            try:
                self.initial['category'] = QuestionCategory.objects.get(name='Uncategorized')
            except QuestionCategory.DoesNotExist:
                pass

    def clean(self):
        cleaned_data = super().clean()
        choices = cleaned_data.get('choices')
        answer = cleaned_data.get('answer')
        # Test parsing choices as JSON list
        try:
            parsed_choices = json.loads(choices)
            # Check parsed_choices is list
            if not isinstance(parsed_choices, list):
                self.add_error('choices', 'Choices must be a valid JSON list')
                return
            # Check duplicate choice
            if len(parsed_choices) != len(set(parsed_choices)):
                self.add_error('choices', 'Choices must be unique')
                return
            # Check have choice more than 4
            if len(parsed_choices) < 4:
                self.add_error('choices', 'Must have more than 4 choices in total')
                return
            # Convert each choice to string
            parsed_choices = [str(c) for c in parsed_choices]
            cleaned_data['choices'] = parsed_choices
        except json.JSONDecodeError:
            self.add_error('choices', 'Choices must be a valid JSON list')
            return
        # Test answer exist in choices
        try:
            parsed_answer = json.loads(answer)
            # Check parsed_answer is list
            if not isinstance(parsed_answer, list):
                self.add_error('answer', 'Answer must be a valid JSON list')
                return
            # Check duplicate answer
            if len(parsed_answer) != len(set(parsed_answer)):
                self.add_error('answer', 'Answer must be unique')
                return
            # Check have answer more than 1
            if len(parsed_answer) < 1:
                self.add_error('answer', 'Must have more than 1 answer')
                return
            # Check answer exist in choices
            if not all(a in parsed_choices for a in parsed_answer):
                self.add_error('answer', 'Answer must be exist in choices')
                return
            # Check all choice - answer is 3
            if len(parsed_choices) - len(parsed_answer) < 3:
                self.add_error('answer', f'The difference between correct and incorrect answers must be of at least 3 (choices: {len(parsed_choices)}, answer: {len(parsed_answer)})')
                return
            # Convert each answer to string
            parsed_answer = [str(a) for a in parsed_answer]
            cleaned_data['answer'] = parsed_answer
        except json.JSONDecodeError:
            self.add_error('answer', 'Answer must be a valid JSON list')
            return
        return cleaned_data


class ImageCustomQuestionForm(forms.Form):
    question = forms.CharField(
        label='Question',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        ),
        help_text='The question of this custom question.'
    )
    choices = MultipleFileField(
        label='Choices',
        widget=MultipleFileInput(
            attrs={
                'class': 'form-control'
            }
        ),
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        help_text='The choices of this custom question. A minimum 4 choices are needed. Supported image formats: jpg, jpeg, png'
    )
    answer = MultipleFileField(
        label='Answer',
        widget=MultipleFileInput(
            attrs={
                'class': 'form-control'
            }
        ),
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        help_text='The answer of this custom question. It must exist in the choices and the difference between correct and incorrect answers must be of at least 3.'
    )
    difficulty_level = forms.CharField(
        label='Difficulty Level',
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            },
            choices=[
                ('easy', 'Easy'),
                ('medium', 'Medium'),
                ('hard', 'Hard')
            ]
        ),
        help_text='The difficulty of the question compared to others in the same category. This affects the question is selected based on a user\'s category score.'
    )
    category = forms.ModelChoiceField(
        label='Category',
        queryset=QuestionCategory.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
        help_text='The category of this custom question.'
    )

    class Meta:
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'category' not in self.initial:
            try:
                self.initial['category'] = QuestionCategory.objects.get(name='Uncategorized')
            except QuestionCategory.DoesNotExist:
                pass

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['choices'] = self.files.getlist('choices')
        cleaned_data['answer'] = self.files.get('answer')
        # get from raw data
        choices = self.files.getlist('choices')
        answer = self.files.getlist('answer')
        # Check have choice more than 4
        if len(choices) < 4:
            self.add_error('choices', 'There must be more than 4 choices')
            return
        # Check duplicate choice
        if len(choices) != len(set(choices)):
            self.add_error('choices', 'Choices must be unique')
            return
        # Check duplicate answer
        if len(answer) != len(set(answer)):
            self.add_error('answer', 'Answer must be unique')
            return
        # Get index of answer in choices
        cleaned_data['answer_len'] = []
        for a in answer:
            try:
                cleaned_data['answer_len'].append([c.name for c in choices].index(a.name))
            except Exception as e:
                print(e)
                self.add_error('answer', f'Answer {a.name} not found in choices')
        # Check all choice - answer is 3
        if len(choices) - len(cleaned_data['answer_len']) < 3:
            self.add_error('answer', 'The difference between correct and incorrect answers must be of at least 3')
            return
        return cleaned_data
