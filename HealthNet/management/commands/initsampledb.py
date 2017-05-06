from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from HealthNet.tests import *
from HealthNet.console import print_status

class Command(BaseCommand):

    def handle(self, *args, **options):
        initialize_database()
