from django.apps import AppConfig


class CommonConfig(AppConfig):
    name = 'test_venta.common'
    verbose_name = "Common"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
