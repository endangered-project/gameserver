from decouple import config
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect

from apps.forms import QuestionModelForm, GameModeForm
from apps.models import QuestionModel, GameMode

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
            question.save()
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


@login_required
@user_passes_test(lambda u: u.is_staff)
def game_mode_list(request):
    return render(request, 'apps/game_mode/list.html', {
        'game_modes': GameMode.objects.all()
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def game_mode_create(request):
    if request.method == 'POST':
        form = GameModeForm(request.POST)
        if form.is_valid():
            GameMode.objects.create(
                name=form.cleaned_data['name'],
                answer_mode=form.cleaned_data['answer_mode']
            )
            messages.success(request, 'Game mode created successfully')
            return redirect('apps_game_mode_list')
    else:
        form = GameModeForm()
    return render(request, 'apps/game_mode/create.html', {
        'form': form
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def game_mode_edit(request, game_mode_id):
    game_mode = GameMode.objects.get(pk=game_mode_id)
    if request.method == 'POST':
        form = GameModeForm(request.POST)
        if form.is_valid():
            game_mode.name = form.cleaned_data['name']
            game_mode.answer_mode = form.cleaned_data['answer_mode']
            game_mode.save()
            messages.success(request, 'Game mode updated successfully')
            return redirect('apps_game_mode_list')
    else:
        form = GameModeForm(initial={
            'name': game_mode.name,
            'answer_mode': game_mode.answer_mode
        })
    return render(request, 'apps/game_mode/edit.html', {
        'form': form,
        'game_mode': game_mode
    })