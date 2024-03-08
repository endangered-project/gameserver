import logging

from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.question import generate_question, FailedToGenerateQuestion

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
