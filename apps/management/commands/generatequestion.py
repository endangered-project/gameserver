import json

from django.core.management import BaseCommand

from apps.question import generate_question


class Command(BaseCommand):
    help = 'Generate a random question'

    def handle(self, *args, **options):
        question = generate_question()
        print(json.dumps(question, indent=4))
