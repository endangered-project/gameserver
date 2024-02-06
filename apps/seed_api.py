from decouple import config
import requests

KNOWLEDGE_BASE_URL = config('KNOWLEDGE_BASE_URL', default='http://localhost:8000')
if KNOWLEDGE_BASE_URL[-1] == '/':
    KNOWLEDGE_BASE_URL = KNOWLEDGE_BASE_URL[:-1]


def get_all_class():
    """
    Get all class in knowledge base
    API endpoint : /api/class
    :return: Class list in JSON format
    """
    url = f'{KNOWLEDGE_BASE_URL}/api/class'
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f'Error when getting all class from knowledge base. Status code: {response.status_code}')
    return response.json()['class']


def get_class(class_id):
    """
    Get class by ID
    API endpoint : /api/class?class={class_id}
    :param class_id: ID of class
    :return: Class in JSON format
    """
    url = f'{KNOWLEDGE_BASE_URL}/api/class?class={class_id}'
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f'Error when getting class from knowledge base. Status code: {response.status_code}')
    return response.json()['class']


def get_property_type_from_class(class_id):
    """
    Get property type from class
    API endpoint : /api/property_type?class={class_id}
    :param class_id: ID of class
    :return: Property type list in JSON format
    """
    url = f'{KNOWLEDGE_BASE_URL}/api/property_type?class={class_id}'
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f'Error when getting property type from class. Status code: {response.status_code}')
    return response.json()['property_type']
