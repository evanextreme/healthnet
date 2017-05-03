from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from HealthNet.tests import *
from HealthNet.console import print_status

class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            settings_warn()
            initialize_database()
            email_test()
            delete_test_objects()
        except KeyboardInterrupt as e:
            print()
            print_status('USERFAIL','KeyboardInterrupt detected. Cleaning up database...')
            delete_test_objects()
            print_status('GOOD','KeyboardInterrupt cleanup successful, database status reset.')
