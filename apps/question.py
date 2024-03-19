import json
import logging
import random

from decouple import config
from django.contrib.auth.models import User

from apps.models import QuestionModel, GameMode, QuestionCategory, UserCategoryWeight, TextCustomQuestion, \
    ImageCustomQuestion
from apps.seed_api import get_instance_from_class, get_instance
from apps.utils import create_weight_from_database

logger = logging.getLogger(__name__)
CURRENT_URL = config('CURRENT_URL')
KNOWLEDGE_BASE_URL = config('KNOWLEDGE_BASE_URL')


class FailedToGenerateQuestion(Exception):
    pass


def get_all_question_mode():
    all_question_mode = []
    if QuestionModel.objects.all().exists():
        all_question_mode.append("seed_question")
    if TextCustomQuestion.objects.all().exists():
        all_question_mode.append("text_custom_question")
    if ImageCustomQuestion.objects.all().exists():
        all_question_mode.append("image_custom_question")
    return all_question_mode


def generate_question(choices: int = 4, try_count: int = 100, specific_question_id: int = None, target_user: User = None, question_mode: str = None, custom_weight: dict = None):
    """
    Generate a question for the user to answer
    :param specific_question_id: Specific question ID to generate if want to generate specific question
    :param choices: Number of choices to generate
    :param try_count: Number of tries to generate question
    :return: Dict of question, choices, and answer
    """
    for i in range(try_count):
        try:
            # random category
            category = QuestionCategory.objects.order_by('?').first()
            if category is None:
                raise FailedToGenerateQuestion("No category found")

            # filter only question that have category in user's weight
            # > 5.0 -> allow medium
            # > 10.0 -> allow hard

            if custom_weight and target_user:
                # We prefer to use custom weight if it's provided more than target_user
                if category.id in custom_weight.keys():
                    weight = custom_weight[category.id]
                else:
                    UserCategoryWeight.objects.create(user=target_user, category=category, weight=0.0)
                    weight = 0.0
            elif target_user and not custom_weight:
                custom_weight = create_weight_from_database(target_user.id)
                try:
                    weight = custom_weight[category.id]
                except KeyError:
                    UserCategoryWeight.objects.create(user=target_user, category=category, weight=0.0)
                    weight = 0.0
            elif not target_user and custom_weight:
                try:
                    weight = custom_weight[category.id]
                except KeyError:
                    weight = 0.0
            else:
                # random 1-10 float
                weight = random.uniform(0.0, 10.0)

            if weight < 5.0:
                difficulty_level = "easy"
            elif weight < 10.0:
                difficulty_level = random.choice(["easy", "medium"])
            else:
                difficulty_level = random.choice(["easy", "medium", "hard"])

            # random between seed_question, text_custom_question, and image_custom_question
            if question_mode:
                if question_mode not in get_all_question_mode():
                    raise FailedToGenerateQuestion(f"Failed to generate question, question mode {question_mode} is not allowed")
                question_mode = question_mode
            else:
                all_question_mode = get_all_question_mode()
                if all_question_mode:
                    question_mode = random.choice(all_question_mode)
                else:
                    raise FailedToGenerateQuestion("No question mode found")

            # random one question
            if question_mode == "seed_question":
                if specific_question_id:
                    try:
                        question = QuestionModel.objects.get(pk=specific_question_id)
                    except QuestionModel.DoesNotExist:
                        raise FailedToGenerateQuestion(f"Failed to generate question, question with ID {specific_question_id} not found")
                else:
                    all_question = QuestionModel.objects.filter(category=category, difficulty_level=difficulty_level)
                    question = random.choice(all_question)
            elif question_mode == "text_custom_question":
                if specific_question_id:
                    try:
                        question = TextCustomQuestion.objects.get(pk=specific_question_id)
                    except TextCustomQuestion.DoesNotExist:
                        raise FailedToGenerateQuestion(f"Failed to generate question, question with ID {specific_question_id} not found")
                else:
                    all_question = TextCustomQuestion.objects.filter(category=category, difficulty_level=difficulty_level)
                    question = random.choice(all_question)
            elif question_mode == "image_custom_question":
                if specific_question_id:
                    try:
                        question = ImageCustomQuestion.objects.get(pk=specific_question_id)
                    except ImageCustomQuestion.DoesNotExist:
                        raise FailedToGenerateQuestion(f"Failed to generate question, question with ID {specific_question_id} not found")
                else:
                    all_question = ImageCustomQuestion.objects.filter(category=category, difficulty_level=difficulty_level)
                    question = random.choice(all_question)
            else:
                raise FailedToGenerateQuestion(f"Failed to generate question, question mode {question_mode} not found")

            # random the game mode
            game_mode = GameMode.objects.order_by('?').first()

            if question is None or game_mode is None:
                raise FailedToGenerateQuestion("No question or game mode found")

            if question_mode == "seed_question":
                if question.answer_mode not in game_mode.allow_answer_mode:
                    raise FailedToGenerateQuestion(f"Failed to generate question, question mode {question.answer_mode} not allowed in game mode {game_mode.name}")

                if question.answer_mode == "single_right":
                    return generate_single_right_question(question, game_mode, choices)
                elif question.answer_mode == "text":
                    return generate_text_question(question, game_mode)
                else:
                    raise FailedToGenerateQuestion(f"Failed to generate question, question mode {question.answer_mode} not found")
            elif question_mode == "text_custom_question":
                if "single_right" not in game_mode.allow_answer_mode:
                    raise FailedToGenerateQuestion(f"Failed to generate question, question mode 'single_right' not allowed in game mode {game_mode.name}")
                return generate_text_custom_question(question, game_mode, choices)
            elif question_mode == "image_custom_question":
                if "single_right" not in game_mode.allow_answer_mode:
                    raise FailedToGenerateQuestion(f"Failed to generate question, question mode 'single_right' not allowed in game mode {game_mode.name}")
                return generate_image_custom_question(question, game_mode, choices)
            else:
                raise FailedToGenerateQuestion(f"Failed to generate question, question mode {question_mode} not found")

        except FailedToGenerateQuestion as e:
            logger.error(f"Failed to generate question: {e}")
            logger.exception(e)
            continue

        except Exception as e:
            logger.error(f"Failed to generate question: {e}")
            logger.exception(e)
            continue
    raise FailedToGenerateQuestion(f"Failed to generate question after {try_count} tries")


def generate_single_right_question(question: QuestionModel, game_mode: GameMode, choices: int = 4):
    """
    Generate a "single right" question
    :param question: QuestionModel instance
    :param game_mode: GameMode instance
    :param choices: Number of choices to generate
    :return: Dict of question, choices, and answer
    """
    if question.answer_mode != "single_right":
        raise FailedToGenerateQuestion(f"Failed to generate question, question mode is not 'text' instead of {question.answer_mode}")

    rendered_question = question.question
    question_properties = question.get_property_in_question()

    instance_list = get_instance_from_class(question.main_class_id)
    # random the instance from the instance list
    question_instance = random.choice(instance_list)
    # try get raw value of question property
    for question_property in question_properties:
        try:
            # find member of list in question_instance['property_values'] that have property_type['name'] ==
            # question_property
            property_value = next((pv for pv in question_instance['property_values'] if
                                   pv['property_type']['name'] == question_property), None)
            rendered_question = rendered_question.replace(
                "{" + question_property + "}",
                property_value['raw_value']
            )
        except StopIteration or KeyError:
            raise FailedToGenerateQuestion(
                f"Failed to generate question, property {question_property} not found in instance")

    choice_list = []
    choice_type = ""

    # before get in while loop, just check instance for creating choice is more than the target choices
    # number (choices-1)
    if len(instance_list) < choices - 1:
        raise FailedToGenerateQuestion(f"Failed to generate question, instance list is less than {choices - 1}")

    # Remove the answer instance from the instance list
    instance_list = [i for i in instance_list if i['id'] != question_instance['id']]

    while len(choice_list) < choices - 1:
        try:
            choice_instance = random.choice(instance_list)
            choice_property_value = next((pv for pv in choice_instance['property_values'] if
                                          pv['property_type']['id'] == question.answer_property_id), None)
            choice_type = choice_property_value['property_type']['raw_type']
            if choice_type == "instance":
                instance = get_instance(choice_property_value['raw_value'])
                if instance["name"] not in choice_list:
                    choice_list.append(instance["name"])
                else:
                    continue
            elif choice_type == "image":
                if KNOWLEDGE_BASE_URL + choice_property_value['raw_value'] not in choice_list:
                    choice_list.append(KNOWLEDGE_BASE_URL + choice_property_value['raw_value'])
                else:
                    continue
            else:
                if choice_property_value['raw_value'] not in choice_list:
                    choice_list.append(choice_property_value['raw_value'])
                else:
                    continue
        except StopIteration or KeyError:
            raise FailedToGenerateQuestion(
                f"Failed to generate question, property ID {question.answer_property_id} not found")
        except Exception as e:
            raise FailedToGenerateQuestion(f"Failed to generate question, {e}")

    # append the answer to the choice in random position
    answer_property_value = next((pv for pv in question_instance['property_values'] if
                                  pv['property_type']['id'] == question.answer_property_id), None)
    if answer_property_value['property_type']['raw_type'] == "instance":
        instance = get_instance(answer_property_value['raw_value'])
        answer_raw_value = instance["name"]
    elif answer_property_value['property_type']['raw_type'] == "image":
        answer_raw_value = KNOWLEDGE_BASE_URL + answer_property_value['raw_value']
    else:
        answer_raw_value = answer_property_value['raw_value']
    choice_list.insert(random.randint(0, len(choice_list)), answer_raw_value)

    return {
        "question": {
            "text": question.question,
            "question_model_instance": question_instance.get('id'),
            "question_property": question_properties,
            "main_class_id": question.main_class_id,
            "answer_property": question.answer_property_id,
            "answer_mode": question.answer_mode
        },
        "question_mode": "seed_question",
        "question_category": question.category.name,
        "rendered_question": rendered_question,
        "game_mode": {
            "name": game_mode.name
        },
        "choices": choice_list,
        "choices_type": choice_type,
        "answer": answer_raw_value,
        "type": choice_type,
        "difficulty_level": question.difficulty_level
    }


def generate_text_question(question: QuestionModel, game_mode: GameMode):
    """
    Generate a "text" question
    :param question: QuestionModel instance
    :param game_mode: GameMode instance
    :return: Dict of question, and answer
    """
    if question.answer_mode != "text":
        raise FailedToGenerateQuestion(f"Failed to generate question, question mode is not 'text' instead of {question.answer_mode}")

    rendered_question = question.question
    question_properties = question.get_property_in_question()

    instance_list = get_instance_from_class(question.main_class_id)
    # random the instance from the instance list
    question_instance = random.choice(instance_list)
    # try get raw value of question property
    for question_property in question_properties:
        try:
            # find member of list in question_instance['property_values'] that have property_type['name'] ==
            # question_property
            property_value = next((pv for pv in question_instance['property_values'] if
                                   pv['property_type']['name'] == question_property), None)
            rendered_question = rendered_question.replace(
                "{" + question_property + "}",
                property_value['raw_value']
            )
        except StopIteration or KeyError:
            raise FailedToGenerateQuestion(
                f"Failed to generate question, property {question_property} not found in instance")

    choice_list = []
    answer_property_value = next((pv for pv in question_instance['property_values'] if
                                  pv['property_type']['id'] == question.answer_property_id), None)
    choice_type = answer_property_value['property_type']['raw_type']

    return {
        "question": {
            "text": question.question,
            "question_model_instance": question_instance.get('id'),
            "question_property": question_properties,
            "main_class_id": question.main_class_id,
            "answer_property": question.answer_property_id,
            "answer_mode": question.answer_mode
        },
        "question_mode": "seed_question",
        "question_category": question.category.name,
        "rendered_question": rendered_question,
        "game_mode": {
            "name": game_mode.name
        },
        "choices": choice_list,
        "choices_type": choice_type,
        "answer": answer_property_value['raw_value'],
        "type": choice_type,
        "difficulty_level": question.difficulty_level
    }


def generate_text_custom_question(question: TextCustomQuestion, game_mode: GameMode, choices: int = 4):
    """
    Generate a "text custom" question
    :param question: TextCustomQuestion instance
    :param game_mode: GameMode instance
    :param choices: Number of choices to generate
    :return: Dict of question, choices, and answer
    """
    if "single_right" not in game_mode.allow_answer_mode:
        raise FailedToGenerateQuestion(f"Failed to generate question, question mode 'single_right' not allowed in game mode {game_mode.name}")

    all_answer = json.loads(question.answer.replace("'", '"'))
    answer = random.choice(all_answer)
    choice_list = json.loads(question.choices.replace("'", '"'))
    if len(choice_list) < choices - 1:
        raise FailedToGenerateQuestion(f"Failed to generate question, choice list is less than {choices - 1}")
    final_choice = [answer]
    while len(final_choice) < choices:
        choice = random.choice(choice_list)
        if choice not in final_choice:
            final_choice.append(choice)

    random.shuffle(final_choice)

    return {
        "question": {
            "text": question.question,
            "answer_mode": "single_right"
        },
        "question_mode": "text_custom_question",
        "question_category": question.category.name,
        "rendered_question": question.question,
        "game_mode": {
            "name": game_mode.name
        },
        "choices": final_choice,
        "choices_type": "text",
        "answer": answer,
        "type": "text",
        "difficulty_level": question.difficulty_level
    }


def generate_image_custom_question(question: ImageCustomQuestion, game_mode: GameMode, choices: int = 4):
    """
    Generate a "image custom" question
    :param question: ImageCustomQuestion instance
    :param game_mode: GameMode instance
    :param choices: Number of choices to generate
    :return: Dict of question, choices, and answer
    """
    if "single_right" not in game_mode.allow_answer_mode:
        raise FailedToGenerateQuestion(f"Failed to generate question, question mode 'single_right' not allowed in game mode {game_mode.name}")

    all_answer = json.loads(question.answer.replace("'", '"'))
    answer = random.choice(all_answer)
    choice_list = json.loads(question.choices.replace("'", '"'))
    if len(choice_list) <= choices - 1:
        raise FailedToGenerateQuestion(f"Failed to generate question, choice list is less than {choices - 1}")
    final_choice = [CURRENT_URL + answer]
    while len(final_choice) < choices:
        choice = random.choice(choice_list)
        if CURRENT_URL + choice not in final_choice:
            final_choice.append(CURRENT_URL + choice)

    random.shuffle(final_choice)

    return {
        "question": {
            "text": question.question,
            "answer_mode": "single_right"
        },
        "question_mode": "image_custom_question",
        "question_category": question.category.name,
        "rendered_question": question.question,
        "game_mode": {
            "name": game_mode.name
        },
        "choices": final_choice,
        "choices_type": "image",
        "answer": CURRENT_URL + answer,
        "type": "image",
        "difficulty_level": question.difficulty_level
    }
