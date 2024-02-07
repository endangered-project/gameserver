from decouple import config
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect

from apps.forms import QuestionModelForm
from apps.models import QuestionModel

KNOWLEDGE_BASE_URL = config('KNOWLEDGE_BASE_URL', default='http://localhost:8000')
if KNOWLEDGE_BASE_URL[-1] == '/':
    KNOWLEDGE_BASE_URL = KNOWLEDGE_BASE_URL[:-1]


def home(request):
    return render(request, 'apps/home.html')


@login_required
@user_passes_test(lambda u: u.is_staff)
def question_list(request):
    return render(request, 'apps/question/list.html', {
        'questions': QuestionModel.objects.all()
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def question_create(request):
    # TODO: make it editable
    if request.method == 'POST':
        form = QuestionModelForm(request.POST)
        if form.is_valid():
            QuestionModel.objects.create(
                main_class_id=form.cleaned_data['main_class_id'],
                question=form.cleaned_data['question'],
                answer_property_id=form.cleaned_data['answer_property_id']
            )
            messages.success(request, 'Question created successfully')
            return redirect('apps_question_list')
    else:
        form = QuestionModelForm()
    return render(request, 'apps/question/create.html', {
        'form': form,
        'knowledge_base_url': KNOWLEDGE_BASE_URL
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def question_edit(request, question_id):
    question = QuestionModel.objects.get(pk=question_id)
    if request.method == 'POST':
        form = QuestionModelForm(request.POST)
        if form.is_valid():
            question.main_class_id = form.cleaned_data['main_class_id']
            question.question = form.cleaned_data['question']
            question.answer_property_id = form.cleaned_data['answer_property_id']
            messages.success(request, 'Question updated successfully')
            return redirect('apps_question_list')
    else:
        form = QuestionModelForm(initial={
            'main_class_id': question.main_class_id,
            'question': question.question,
            'answer_property_id': question.answer_property_id
        })
    return render(request, 'apps/question/edit.html', {
        'form': form,
        'knowledge_base_url': KNOWLEDGE_BASE_URL,
        'question': question
    })
