from django.contrib.auth.models import User

from apps.models import QuestionCategory, UserCategoryWeight, GameQuestion, Game


def create_all_weighted():
    """
    Create all weighted for all users and categories
    """
    for user in User.objects.all():
        for category in QuestionCategory.objects.all():
            if not UserCategoryWeight.objects.filter(user=user, category=category).exists():
                UserCategoryWeight.objects.create(user=user, category=category, weight=0.0)


def create_weight_from_game(game_id):
    """
    Create weight dict applied from game history
    :param game_id: Game ID
    :return: Weight dict
    """
    question = GameQuestion.objects.filter(game_id=game_id, answered=True)
    weight = {}
    for q in question:
        if q.question.category.id in weight.keys():
            weight[q.question.category.id] += q.get_weight()
        else:
            weight[q.question.category.id] = q.get_weight()
    return weight


def create_weight_from_database(user_id):
    """
    Create weight dict applied from UserCategoryWeight
    :param user_id: User ID
    :return: Weight dict
    """
    all_weight = UserCategoryWeight.objects.filter(user_id=user_id)
    weight = {}
    for w in all_weight:
        weight[w.category.id] = w.weight
    return weight


def create_total_weight_with_game(game_id):
    """
    Create total weight from history and in game
    :param game_id: Game ID
    :return: Weight dict
    """
    game_weight = create_weight_from_game(game_id)
    game = Game.objects.get(id=game_id)
    history_weight = create_weight_from_database(game.user_id)
    weight = history_weight
    for k, v in game_weight.items():
        if k in weight.keys():
            weight[k] += v
        else:
            weight[k] = v
    return weight


def calculate_total_score(game_id):
    """
    Calculate total score for game
    :param game_id: Game ID
    :return: score
    """
    valid_question = GameQuestion.objects.filter(is_true=True, answered=True, game_id=game_id)
    total_score = 0
    for question in valid_question:
        difficulty = question.question.difficulty_level
        if difficulty == 'easy':
            total_score += 50
        elif difficulty == 'medium':
            total_score += 100
        else:
            total_score += 200
    return total_score


def generate_leaderboard():
    """
    Generate leaderboard
    :return: Leaderboard dict
    """
    leaderboard = {}
    for user in User.objects.all():
        leaderboard[user.username] = 0
        for game in Game.objects.filter(user=user, finished=True, completed=True):
            if game.score > leaderboard[user.username]:
                leaderboard[user.username] = game.score
    leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1], reverse=True))
    leaderboard = [{"username": k, "score": v, "rank": i + 1, "user_id": User.objects.get(username=k).id, "profile_picture": User.objects.get(username=k).profile.get_full_avatar_url()} for i, (k, v) in enumerate(leaderboard.items())]
    return leaderboard


def get_user_rank(user_id) -> int:
    """
    Get user's rank
    :param user_id: User ID
    :return: Rank
    """
    leaderboard = generate_leaderboard()
    for i, user in enumerate(leaderboard):
        if user['user_id'] == user_id:
            return i + 1
    return 0


def get_user_highscore(user_id) -> int:
    """
    Get user's highscore
    :param user_id: User ID
    :return: Highscore
    """
    leaderboard = generate_leaderboard()
    for user in leaderboard:
        if user['user_id'] == user_id:
            return user['score']
    return 0
