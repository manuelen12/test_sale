from django.apps import AppConfig


class SalesConfig(AppConfig):
    name = 'test_venta.sales'
    verbose_name = "Sales"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
