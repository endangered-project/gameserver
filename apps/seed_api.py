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


def get_instance_from_class(class_id):
    """
    Get instance from class
    API endpoint : /api/instance?class={class_id}
    :param class_id: ID of class
    :return: Instance list in JSON format
    """
    url = f'{KNOWLEDGE_BASE_URL}/api/instance?class={class_id}'
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f'Error when getting instance from class. Status code: {response.status_code}')
    return response.json()['instance']


def get_instance(instance_id):
    """
    Get instance by ID
    API endpoint : /api/instance/{instance_id}
    :param instance_id: ID of instance
    :return: Instance in JSON format
    """
    url = f'{KNOWLEDGE_BASE_URL}/api/instance/{instance_id}'
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f'Error when getting instance from knowledge base. Status code: {response.status_code}')
    return response.json()
