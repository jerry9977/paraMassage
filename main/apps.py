from django.apps import AppConfig
from django.core.signals import request_finished


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from main.signals import handlers
        request_finished.connect(handlers.history_post_save, dispatch_uid="history_post_save")
        request_finished.connect(handlers.client_post_save, dispatch_uid="client_post_save")