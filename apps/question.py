import logging
import random

from apps.models import QuestionModel, GameMode
from apps.seed_api import get_instance_from_class

logger = logging.getLogger(__name__)


class FailedToGenerateQuestion(Exception):
    pass


def generate_question(choices: int = 4, try_count: int = 10):
    """
    Generate a question for the user to answer
    :param choices: Number of choices to generate
    :param try_count: Number of tries to generate question
    :return: Dict of question, choices, and answer
    """
    for i in range(try_count):
        try:
            # random one question
            question = QuestionModel.objects.order_by('?').first()
            # random the game mode
            game_mode = GameMode.objects.order_by('?').first()

            if question is None or game_mode is None:
                raise FailedToGenerateQuestion("No question or game mode found")

            if question.answer_mode not in game_mode.allow_answer_mode:
                raise FailedToGenerateQuestion(f"Failed to generate question, question mode {question.answer_mode} not allowed in game mode {game_mode.name}")

            if question.answer_mode == "single_right":
                return generate_single_right_question(question, game_mode, choices)
            elif question.answer_mode == "text":
                return generate_text_question(question, game_mode)


        except FailedToGenerateQuestion as e:
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

    while len(choice_list) < choices - 1:
        try:
            choice_instance = random.choice(instance_list)
            choice_property_value = next((pv for pv in choice_instance['property_values'] if
                                          pv['property_type']['id'] == question.answer_property_id), None)
            choice_type = choice_property_value['property_type']['raw_type']
            if choice_property_value['raw_value'] not in choice_list:
                choice_list.append(choice_property_value['raw_value'])
        except StopIteration or KeyError:
            raise FailedToGenerateQuestion(
                f"Failed to generate question, property ID {question.answer_property_id} not found")

    # append the answer to the choice in random position
    answer_property_value = next((pv for pv in question_instance['property_values'] if
                                  pv['property_type']['id'] == question.answer_property_id), None)
    choice_list.insert(random.randint(0, len(choice_list)), answer_property_value['raw_value'])

    return {
        "question": {
            "text": question.question,
            "question_model_instance": question_instance.get('id'),
            "question_property": question_properties,
            "main_class_id": question.main_class_id,
            "answer_property": question.answer_property_id,
            "answer_mode": question.answer_mode
        },
        "rendered_question": rendered_question,
        "game_mode": {
            "name": game_mode.name
        },
        "choices": choice_list,
        "answer": answer_property_value['raw_value'],
        "type": choice_type
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
    answer_property_value = next((pv for pv in question_instance['property_values'] if pv['property_type']['id'] == question.answer_property_id), None)
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
        "rendered_question": rendered_question,
        "game_mode": {
            "name": game_mode.name
        },
        "choices": choice_list,
        "answer": answer_property_value['raw_value'],
        "type": choice_type
    }
