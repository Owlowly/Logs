from django.apps import AppConfig


class LearningLogsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'learning_logs'

    def ready(self):
        # import signals handler
        import learning_logs.signals
