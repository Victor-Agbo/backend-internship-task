from django.apps import AppConfig


class CaloriesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "calories"

    def ready(self):
        from .groups import create_groups

        create_groups()
        from .models import User
        from rest_framework.authtoken.models import Token

        users = User.objects.all()
        for user in users:
            Token.objects.get_or_create(user=user)
