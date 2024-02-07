from django import forms

from apps.models import QuestionModel, ANSWER_MODE_CHOICES
from apps.seed_api import get_all_class, get_property_type_from_class


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

    class Meta:
        model = QuestionModel
        fields = '__all__'

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
        widget=forms.SelectMultiple(
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
