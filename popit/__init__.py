from django.apps import AppConfig


class PopitConfig(AppConfig):
    name = "popit"
    verbose_name = "popit"

    def ready(self):
        import popit.signals.handlers