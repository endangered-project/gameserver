from django.contrib.auth.models import User

from apps.models import QuestionCategory, UserCategoryWeight


def create_all_weighted():
    """
    Create all weighted for all users and categories
    """
    for user in User.objects.all():
        for category in QuestionCategory.objects.all():
            if not UserCategoryWeight.objects.filter(user=user, category=category).exists():
                UserCategoryWeight.objects.create(user=user, category=category, weight=0.0)
