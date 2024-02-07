import json

from django.core.management import BaseCommand

from apps.question import generate_question


class Command(BaseCommand):
    help = 'Disconnect user from channel layer if subscription is expired'

    def handle(self, *args, **options):
        question = generate_question()
        print(json.dumps(question, indent=4))
