import django
import os

# Django-Umgebung konfigurieren
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coderr.settings')
django.setup()

from django.contrib.auth.models import User
from backend_app.models import UserProfile

def create_user(username, email, password, user_type):
    if User.objects.filter(username=username).exists():
        print(f"User '{username}' already exists!")
        return None
    if User.objects.filter(email=email).exists():
        print(f"Email '{email}' is already in use!")
        return None

    # Erstelle den User ohne 'user_type'
    user = User.objects.create_user(username=username, email=email, password=password)

    # Setze den Typ des UserProfiles (so wie im Serializer)
    user.userprofile.type = user_type
    user.userprofile.save()

    print(f"User '{username}' created successfully with type '{user_type}'!")
    return user

if __name__ == "__main__":
    users_to_create = [
        {"username": "andrey", "email": "customer@example.com", "password": "asdasd", "user_type": "customer"},
        {"username": "kevin", "email": "business@example.com", "password": "asdasd24", "user_type": "business"},
    ]

    for user_data in users_to_create:
        create_user(**user_data)
