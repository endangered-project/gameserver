import json
import logging

from decouple import config
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect

from apps.forms import QuestionModelForm, GameModeForm, QuestionCategoryForm, TextCustomQuestionForm, \
    ImageCustomQuestionForm
from apps.models import QuestionModel, GameMode, QuestionCategory, TextCustomQuestion, ImageCustomQuestion, Game, \
    GameQuestion
from apps.question import generate_question
from apps.utils import create_all_weighted, generate_leaderboard, get_user_rank, get_user_highscore

KNOWLEDGE_BASE_URL = config('KNOWLEDGE_BASE_URL', default='http://localhost:8000')
if KNOWLEDGE_BASE_URL[-1] == '/':
    KNOWLEDGE_BASE_URL = KNOWLEDGE_BASE_URL[:-1]

logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'apps/home.html', {
        'user_obj': request.user if request.user.is_authenticated else None,
        'user_rank': get_user_rank(request.user.id) if request.user.is_authenticated else 0,
        'user_high_score': get_user_highscore(request.user.id) if request.user.is_authenticated else 0
    })


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
def question_toggle_active(request, question_id):
    try:
        question = QuestionModel.objects.get(pk=question_id)
    except QuestionModel.DoesNotExist:
        messages.error(request, 'Question not found')
        return redirect('apps_question_list')
    question.active = not question.active
    question.save()
    messages.success(request, 'Question active status updated successfully')
    return redirect('apps_question_list')


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
    question_mode = request.GET.get('question_mode')
    try:
        if id:
            question = generate_question(specific_question_id=id, question_mode=question_mode if question_mode else None)
        else:
            question = generate_question()
        indented_html_question = str(json.dumps(question, indent=4)).replace('\n', '<br>').replace(' ', '&nbsp;')
        exception_message = None
    except Exception as e:
        logger.exception(e)
        question = None
        indented_html_question = None
        exception_message = str(e)
    return render(request, 'apps/question_generator_test.html', {
        "question": question,
        "exception_message": exception_message,
        "indented_html_question": indented_html_question
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def text_custom_question_list(request):
    return render(request, 'apps/text_custom_question/list.html', {
        'questions': TextCustomQuestion.objects.all()
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def text_custom_question_create(request):
    if request.method == 'POST':
        form = TextCustomQuestionForm(request.POST)
        if form.is_valid():
            TextCustomQuestion.objects.create(
                question=form.cleaned_data['question'],
                choices=form.cleaned_data['choices'],
                answer=form.cleaned_data['answer'],
                difficulty_level=form.cleaned_data['difficulty_level'],
                category=form.cleaned_data['category']
            )
            messages.success(request, 'Question created successfully')
            return redirect('apps_text_custom_question_list')
    else:
        form = TextCustomQuestionForm()
    return render(request, 'apps/text_custom_question/create.html', {
        'form': form
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def text_custom_question_edit(request, question_id):
    try:
        question = TextCustomQuestion.objects.get(pk=question_id)
    except TextCustomQuestion.DoesNotExist:
        messages.error(request, 'Question not found')
        return redirect('apps_text_custom_question_list')
    if request.method == 'POST':
        form = TextCustomQuestionForm(request.POST)
        if form.is_valid():
            question.question = form.cleaned_data['question']
            question.choices = form.cleaned_data['choices']
            question.answer = form.cleaned_data['answer']
            question.difficulty_level = form.cleaned_data['difficulty_level']
            question.category = form.cleaned_data['category']
            question.save()
            messages.success(request, 'Question updated successfully')
            return redirect('apps_text_custom_question_list')
    else:
        form = TextCustomQuestionForm(initial={
            'question': question.question,
            'choices': question.choices.replace("'", '"'),
            'answer': question.answer.replace("'", '"'),
            'category': question.category
        })
    return render(request, 'apps/text_custom_question/edit.html', {
        'form': form,
        'question': question
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def text_custom_question_toggle_active(request, question_id):
    try:
        question = TextCustomQuestion.objects.get(pk=question_id)
    except TextCustomQuestion.DoesNotExist:
        messages.error(request, 'Question not found')
        return redirect('apps_text_custom_question_list')
    question.active = not question.active
    question.save()
    messages.success(request, 'Question active status updated successfully')
    return redirect('apps_text_custom_question_list')


@login_required
@user_passes_test(lambda u: u.is_staff)
def text_custom_question_view(request, question_id):
    try:
        question = TextCustomQuestion.objects.get(pk=question_id)
    except ImageCustomQuestion.DoesNotExist:
        messages.error(request, 'Question not found')
        return redirect('apps_text_custom_question_list')
    return render(request, 'apps/text_custom_question/view.html', {
        'question': question,
        'choice_list': json.loads(question.choices.replace("'", '"'))
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def image_custom_question_list(request):
    return render(request, 'apps/image_custom_question/list.html', {
        'questions': ImageCustomQuestion.objects.all()
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def image_custom_question_create(request):
    if request.method == 'POST':
        form = ImageCustomQuestionForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            image_choice = []
            for image in request.FILES.getlist('choices'):
                saved_path = default_storage.save(f'custom_question/{image.name}', image)
                image_choice.append(default_storage.url(saved_path))
            answer_choice = []
            for answer in cleaned_data['answer_len']:
                answer_choice.append(image_choice[answer])
            ImageCustomQuestion.objects.create(
                question=form.cleaned_data['question'],
                choices=json.dumps(image_choice),
                answer=json.dumps(answer_choice),
                difficulty_level=form.cleaned_data['difficulty_level'],
                category=form.cleaned_data['category']
            )
            messages.success(request, 'Question created successfully')
            return redirect('apps_image_custom_question_list')
    else:
        form = ImageCustomQuestionForm()
    return render(request, 'apps/image_custom_question/create.html', {
        'form': form
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def image_custom_question_edit(request, question_id):
    try:
        question = ImageCustomQuestion.objects.get(pk=question_id)
    except ImageCustomQuestion.DoesNotExist:
        messages.error(request, 'Question not found')
        return redirect('apps_image_custom_question_list')
    if request.method == 'POST':
        form = ImageCustomQuestionForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            question.question = form.cleaned_data['question']
            question.category = form.cleaned_data['category']
            # save image from form (choices)
            choices = []
            for image in request.FILES.getlist('choices'):
                saved_path = default_storage.save(f'custom_question/{image.name}', image)
                choices.append(default_storage.url(saved_path))
            question.choices = json.dumps(choices)
            answers = []
            for answer in cleaned_data['answer_len']:
                answers.append(choices[answer])
            question.answer = json.dumps(answers)
            question.difficulty_level = form.cleaned_data['difficulty_level']
            question.save()
            messages.success(request, 'Question updated successfully')
            return redirect('apps_image_custom_question_list')
    else:
        form = ImageCustomQuestionForm(initial={
            'question': question.question,
            'category': question.category
        })
    return render(request, 'apps/image_custom_question/edit.html', {
        'form': form,
        'question': question
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def image_custom_question_toggle_active(request, question_id):
    try:
        question = ImageCustomQuestion.objects.get(pk=question_id)
    except ImageCustomQuestion.DoesNotExist:
        messages.error(request, 'Question not found')
        return redirect('apps_image_custom_question_list')
    question.active = not question.active
    question.save()
    messages.success(request, 'Question active status updated successfully')
    return redirect('apps_image_custom_question_list')


# TODO: Add breadcrumb navigation


@login_required
@user_passes_test(lambda u: u.is_staff)
def image_custom_question_view(request, question_id):
    try:
        question = ImageCustomQuestion.objects.get(pk=question_id)
    except ImageCustomQuestion.DoesNotExist:
        messages.error(request, 'Question not found')
        return redirect('apps_image_custom_question_list')
    return render(request, 'apps/image_custom_question/view.html', {
        'question': question,
        'choice_list': json.loads(question.choices)
    })


def leaderboard(request):
    return render(request, 'apps/leaderboard.html', {
        'leaderboard': generate_leaderboard()
    })


@login_required
def profile(request):
    return redirect('apps_user_profile', user_id=request.user.id)


def user_profile(request, user_id):
    try:
        user_obj = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'User not found')
        return redirect('apps_home')
    return render(request, 'apps/user_profile.html', {
        'user_obj': user_obj,
        'user_rank': get_user_rank(user_id),
        'user_high_score': get_user_highscore(user_id),
        'history': Game.objects.filter(user=user_obj, finished=True, completed=True).order_by('-end_time')
    })


def play_history(request, game_id):
    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        messages.error(request, 'Game not found')
        return redirect('apps_home')
    if not (game.finished and game.completed):
        messages.error(request, 'Game not found')
        return redirect('apps_home')
    question_history_list = []
    for question in GameQuestion.objects.filter(game=game, answered=True).order_by('id'):
        question_history_list.append({
            'question': question.question.question,
            'question_mode': question.question.question_mode,
            'choices': json.loads(question.question.choice.replace("'", '"')),
            'answer': question.question.answer,
            'selected': question.selected,
            'answered': question.answered,
            'is_true': question.is_true,
            'type': question.question.type,
            'full_json': question.question.full_json
        })
    return render(request, 'apps/play_history.html', {
        'game': game,
        'question_list': question_history_list,
        'right': GameQuestion.objects.filter(game=game, answered=True, is_true=True).count(),
        'wrong': GameQuestion.objects.filter(game=game, answered=True, is_true=False).count(),
        'knowledge_base_url': KNOWLEDGE_BASE_URL
    })
