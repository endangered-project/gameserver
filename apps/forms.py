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
        help_text='Main class of knowledge base that will be used to render the question'
    )
    question = forms.CharField(
        label='Question',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        ),
        max_length=1000,
        help_text='Question template that will be rendered, use {property_name} to use the property'
    )
    answer_property_id = forms.CharField(
        label='Answer Property',
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
        help_text='Property that will be used to render the choices in the question'
    )
    answer_mode = forms.CharField(
        label='Answer Mode',
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            },
            choices=ANSWER_MODE_CHOICES
        ),
        help_text='Answer mode of this question, this will be used to render the choices',
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
        help_text='Difficulty level of this question, this will be used with the score weight on rendering the question',
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
        help_text='Category of this question, this will be used to measure the weight of the question on selecting the question'
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
                self.add_error('question', f'Property {p} is not exist in main class')
        # check answer property exist
        print(all_property_name)
        if answer_property_id not in all_property_id:
            self.add_error('answer_property_id', 'Answer property is not exist')


class GameModeForm(forms.Form):
    name = forms.CharField(
        label='Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
        help_text='Name of game mode',
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
        help_text='Answer mode that allowed in this game mode',
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
        help_text='Name of the category'
    )
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        ),
        help_text='Description of the category',
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
        help_text='Question of this custom question'
    )
    choices = forms.CharField(
        label='Choices',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        ),
        help_text='Choices of this custom question in JSON list format, example: ["choice1", "choice2", "choice3", "choice4"]. Minimum 4 choices'
    )
    answer = forms.CharField(
        label='Answer',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
        help_text='Answer of this custom question'
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
        help_text='Difficulty level of this question, this will be used with the score weight on rendering the question'
    )
    category = forms.ModelChoiceField(
        label='Category',
        queryset=QuestionCategory.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
        help_text='Category of this custom question'
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
            # Check have choice more than 4
            if len(parsed_choices) < 4:
                self.add_error('choices', 'Choices must have more than 4')
                return
            # Convert each choice to string
            parsed_choices = [str(c) for c in parsed_choices]
            cleaned_data['choices'] = parsed_choices
        except json.JSONDecodeError:
            self.add_error('choices', 'Choices must be a valid JSON list')
            return
        # Test answer exist in choices
        if answer not in parsed_choices:
            self.add_error('answer', 'Answer must be exist in choices')
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
        help_text='Question of this custom question'
    )
    # upload multiple images
    choices = MultipleFileField(
        label='Choices',
        widget=MultipleFileInput(
            attrs={
                'class': 'form-control'
            }
        ),
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        help_text='Choices of this custom question in image format, minimum 4 choices (jpg, jpeg, png)'
    )
    answer = forms.ImageField(
        label='Answer',
        widget=forms.FileInput(
            attrs={
                'class': 'form-control'
            }
        ),
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        help_text='Answer of this custom question in image format (jpg, jpeg, png), the answer must be exist in choices'
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
        help_text='Difficulty level of this question, this will be used with the score weight on rendering the question'
    )
    category = forms.ModelChoiceField(
        label='Category',
        queryset=QuestionCategory.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
        help_text='Category of this custom question'
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
        answer = self.files.get('answer')
        # Check have choice more than 4
        if len(choices) < 4:
            self.add_error('choices', 'Choices must have more than 4')
            return
        # Test answer exist in choices (check by filename)
        if answer.name not in [c.name for c in choices]:
            self.add_error('answer', 'Answer must be exist in choices')
            return
        # Save index of answer in choices
        cleaned_data['answer_len'] = [c.name for c in choices].index(answer.name)
        return cleaned_data
