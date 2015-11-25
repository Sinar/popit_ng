from django.apps import AppConfig

default_app_config = 'popit.PopitConfig'

class PopitConfig(AppConfig):
    name = "popit"
    verbose_name = "popit"

    def ready(self):
        import popit.signals.handlers