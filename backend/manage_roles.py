import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django

django.setup()

from core.models import Role

roles = ('admin', 'member')

for role in roles:
    Role.objects.get_or_create(name=role)