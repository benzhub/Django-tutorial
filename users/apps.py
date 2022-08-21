from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # app 中必須加入signal，執行的時候才有辦法觸發signals.py的內容
    def ready(self):
        import users.signals
