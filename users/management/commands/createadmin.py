# users/management/commands/createadmin.py
from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Создает первого администратора'
    
    def handle(self, *args, **options):
        if not User.objects.exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@localhost',
                password='system',
                is_approved=True
            )
            self.stdout.write('Суперпользователь создан!')