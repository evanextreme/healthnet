from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            print('Creating root user')
            admin = User.objects.create_superuser(email='pleasechange@admin.com', username='root', password='admin')
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')
