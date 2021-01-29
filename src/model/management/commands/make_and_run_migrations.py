from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        os.system('python manage.py makemigrations && python manage.py migrate')
