import json
import logging

from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apis.serializers import AnswerQuestionSerializer
from apps.models import Game, GameQuestion, QuestionHistory, QuestionCategory, GameMode
from apps.question import generate_question, FailedToGenerateQuestion
from apps.utils import create_total_weight_with_game, calculate_total_score
from users.models import Profile

logger = logging.getLogger(__name__)


@api_view(['GET'])
def get_random_question(request):
    """
    View for return a random question in JSON format, will also use user's preference if user is authenticated.
    """
    try:
        if request.user.is_authenticated:
            question = generate_question(target_user=request.user)
        else:
            question = generate_question()
        return Response(question)
    except FailedToGenerateQuestion as e:
        logger.error(f'Failed to generate question for user {request.user} (FailedToGenerateQuestion) with error: {str(e)}')
        logger.exception(e)
        return Response({
            'message': str(e)
        }, status=400)
    except Exception as e:
        logger.error(f'Error when getting random question for user {request.user} with error: {str(e)}')
        logger.exception(e)
        return Response({
            'message': 'Internal server error'
        }, status=500)


@api_view(['POST'])
def start_new_game(request):
    """
    Start a new game for user
    """
    if not request.user.is_authenticated:
        return Response({
            'message': 'User is not authenticated'
        }, status=401)
    if Game.objects.filter(finished=False):
        for game in Game.objects.filter(finished=False):
            game.finished = True
            game.completed = False
            game.end_time = timezone.now()
            game.save()
    game = Game.objects.create(
        user=request.user
    )
    return Response({
        'message': 'Game started successfully',
        'game_id': game.id
    })


@api_view(['POST'])
def get_new_question(request):
    """
    Get a new question for user
    """
    if not request.user.is_authenticated:
        return Response({
            'message': 'User is not authenticated'
        }, status=401)
    try:
        # find running game
        game = Game.objects.filter(user=request.user, finished=False).first()
        if not game:
            return Response({
                'message': 'No game is running'
            }, status=400)
        # find question that's not answered yet
        question = GameQuestion.objects.filter(game=game, answered=False).first()
        if question:
            return Response({
                'message': 'There are questions left',
            }, status=400)
        # generate new question
        random_question = generate_question(target_user=request.user, custom_weight=create_total_weight_with_game(game.id))
        new_question = QuestionHistory.objects.create(
            question_mode=random_question['question_mode'],
            category=QuestionCategory.objects.get(name=random_question['question_category']),
            difficulty_level=random_question['difficulty_level'],
            question=random_question['rendered_question'],
            choice=random_question['choices'],
            answer=random_question['answer'],
            type=random_question['type'],
            full_json=random_question
        )
        game_question = GameQuestion.objects.create(
            game=game,
            question=new_question,
            game_mode=GameMode.objects.get(name=random_question['game_mode']['name'])
        )
        return Response({
            'message': 'New question generated',
            'question_id': new_question.id,
            'game_mode': game_question.game_mode.name,
            'question': random_question,
            'choice': new_question.choice,
            'answer': new_question.answer
        })
    except FailedToGenerateQuestion as e:
        logger.error(f'Failed to generate question for user {request.user} (FailedToGenerateQuestion) with error: {str(e)}')
        logger.exception(e)
        return Response({
            'message': str(e)
        }, status=400)
    except Exception as e:
        logger.error(f'Error when getting new question for user {request.user} with error: {str(e)}')
        logger.exception(e)
        return Response({
            'message': 'Internal server error'
        }, status=500)


@api_view(['POST'])
def answer_question(request):
    """
    Answer a question for user
    """
    if not request.user.is_authenticated:
        return Response({
            'message': 'User is not authenticated'
        }, status=401)
    try:
        payload = AnswerQuestionSerializer(data=request.data)
        if payload.is_valid():
            # find running game
            game = Game.objects.filter(user=request.user, finished=False).first()
            if not game:
                return Response({
                    'message': 'No game is running'
                }, status=400)
            # find question that's not answered yet
            question = GameQuestion.objects.filter(game=game, answered=False).first()
            if not question:
                return Response({
                    'message': 'No question to answer'
                }, status=400)
            if question.question.answer == payload.data['answer']:
                question.is_true = True
                question.answered = True
                question.save()
                is_true = True
            else:
                question.is_true = False
                question.answered = True
                question.save()
                is_true = False
            # Calculate all weight and score of this game
            game.selected = payload.data['answer']
            game.weight = create_total_weight_with_game(game.id)
            game.score = calculate_total_score(game.id)
            game.save()
            # Check for end game
            if game.has_lose():
                game.finished = True
                game.completed = True
                game.end_time = timezone.now()
            game.save()
            if is_true:
                return Response({
                    'message': "Right answer",
                    'score': question.get_score()
                })
            else:
                return Response({
                    'message': "Wrong answer",
                    'score': 0
                })
        else:
            return Response({
                'message': 'Invalid payload',
                'score': 0,
                'errors': payload.errors
            }, status=400)
    except Exception as e:
        logger.error(f'Error when answering question for user {request.user} with error: {str(e)}')
        logger.exception(e)
        return Response({
            'message': 'Internal server error'
        }, status=500)


@api_view(['GET'])
def get_user_info(request):
    """
    Get user info
    """
    if not request.user.is_authenticated:
        return Response({
            'message': 'User is not authenticated'
        }, status=401)
    profile = Profile.objects.get(user=request.user)
    return Response({
        'username': request.user.username,
        'profile_picture': profile.get_full_avatar_url()
    })
