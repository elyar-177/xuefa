from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = '创建超级管理员账户'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123456',
                nickname='管理员'
            )
            self.stdout.write(self.style.SUCCESS('超级管理员创建成功'))
