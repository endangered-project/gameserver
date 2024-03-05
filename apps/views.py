import logging

from decouple import config
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect

from apps.forms import QuestionModelForm, GameModeForm, QuestionCategoryForm
from apps.models import QuestionModel, GameMode, QuestionCategory
from apps.question import generate_question
from apps.utils import create_all_weighted

KNOWLEDGE_BASE_URL = config('KNOWLEDGE_BASE_URL', default='http://localhost:8000')
if KNOWLEDGE_BASE_URL[-1] == '/':
    KNOWLEDGE_BASE_URL = KNOWLEDGE_BASE_URL[:-1]

logger = logging.getLogger(__name__)


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
    if request.method == 'POST':
        form = QuestionModelForm(request.POST)
        if form.is_valid():
            QuestionModel.objects.create(
                main_class_id=form.cleaned_data['main_class_id'],
                question=form.cleaned_data['question'],
                answer_property_id=form.cleaned_data['answer_property_id'],
                answer_mode=form.cleaned_data['answer_mode'],
                difficulty_level=form.cleaned_data['difficulty_level'],
                category=form.cleaned_data['category']
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
    try:
        question = QuestionModel.objects.get(pk=question_id)
    except QuestionModel.DoesNotExist:
        messages.error(request, 'Question not found')
        return redirect('apps_question_list')
    if request.method == 'POST':
        form = QuestionModelForm(request.POST)
        if form.is_valid():
            question.main_class_id = form.cleaned_data['main_class_id']
            question.question = form.cleaned_data['question']
            question.answer_property_id = form.cleaned_data['answer_property_id']
            question.answer_mode = form.cleaned_data['answer_mode']
            question.difficulty_level = form.cleaned_data['difficulty_level']
            question.category = form.cleaned_data['category']
            question.save()
            messages.success(request, 'Question updated successfully')
            return redirect('apps_question_list')
    else:
        form = QuestionModelForm(initial={
            'main_class_id': question.main_class_id,
            'question': question.question,
            'answer_property_id': question.answer_property_id,
            'answer_mode': question.answer_mode,
            'difficulty_level': question.difficulty_level,
            'category': question.category
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
                allow_answer_mode=form.cleaned_data['allow_answer_mode']
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
    try:
        game_mode = GameMode.objects.get(pk=game_mode_id)
    except GameMode.DoesNotExist:
        messages.error(request, 'Game mode not found')
        return redirect('apps_game_mode_list')
    if request.method == 'POST':
        form = GameModeForm(request.POST)
        if form.is_valid():
            game_mode.name = form.cleaned_data['name']
            game_mode.allow_answer_mode = form.cleaned_data['allow_answer_mode']
            game_mode.save()
            messages.success(request, 'Game mode updated successfully')
            return redirect('apps_game_mode_list')
    else:
        form = GameModeForm(initial={
            'name': game_mode.name,
            'allow_answer_mode': game_mode.allow_answer_mode
        })
    return render(request, 'apps/game_mode/edit.html', {
        'form': form,
        'game_mode': game_mode
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def question_category_list(request):
    return render(request, 'apps/category/list.html', {
        'categories': QuestionCategory.objects.all()
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def question_category_create(request):
    if request.method == 'POST':
        form = QuestionCategoryForm(request.POST)
        form.save()
        create_all_weighted()
        messages.success(request, 'Category created successfully')
        return redirect('apps_question_category_list')
    else:
        form = QuestionCategoryForm()
    return render(request, 'apps/category/create.html', {
        'form': form
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def question_category_edit(request, category_id):
    try:
        category = QuestionCategory.objects.get(pk=category_id)
    except QuestionCategory.DoesNotExist:
        messages.error(request, 'Category not found')
        return redirect('apps_question_category_list')
    if request.method == 'POST':
        form = QuestionCategoryForm(request.POST, instance=category)
        form.save()
        messages.success(request, 'Category updated successfully')
        return redirect('apps_question_category_list')
    else:
        form = QuestionCategoryForm(instance=category)
    return render(request, 'apps/category/edit.html', {
        'form': form,
        'category': category
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def question_generator_test(request):
    id = request.GET.get('id')
    try:
        if id:
            question = generate_question(specific_question_id=id)
        else:
            question = generate_question()
        exception_message = None
    except Exception as e:
        logger.exception(e)
        question = None
        exception_message = str(e)
    return render(request, 'apps/question_generator_test.html', {
        "question": question,
        "exception_message": exception_message
    })
