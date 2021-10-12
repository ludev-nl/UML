from django.core.management.base import BaseCommand
from django.core import management
import threading
import os

class Command(BaseCommand):
    def runCommands(self):
        management.call_command('makemigrations')
        management.call_command('migrate')

    def handle(self, *args, **options):
        th = threading.Thread(target=self.runCommands)
        th.start()
