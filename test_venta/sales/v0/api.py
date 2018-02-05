# Stdlib imports
from json import loads
# Core Django imports
from django.conf import settings
from django.contrib.auth import get_user_model
# Third-party app imports
# Imports from your apps
from test_venta.common.utils import Base
from test_venta.sales.models import Sales
# from test_venta.sales.models import Rentals, Bike, PriceByFrecuency

User = get_user_model()


class Controller (Base):
    def __init__(self, request):
        Base.__init__(self)
        self.request = request
        self.error = {}
        self.result = []
        self.url_api = settings.HTTP+self.request.META['HTTP_HOST']+"/api/v0/"
        self.data = self.valid_data()

    def valid_sale(self, kwargs):
        __valid = [
            'user_id', 'amount',
        ]

        if not self._list_int_info(kwargs, __valid):
            return
        try:
            self.user = User.objects.get(id=kwargs['user_id'])
        except:
            self._error_info("user", "it is not exist")
            return

        return True

    def create_sale(self):

        if not self.valid_sale(self.data):
            return

        self.export_attr(Sales, self.data)
        if self.user.status == 2:
            self.values['status'] = True
        else:
            self.values['status'] = False

        x = Sales.objects.create(**self.values)

        self.get_sale(x.id)

    def get_sale(self, pk=None):

        __filters = loads(self.request.GET.get('filters', "{}"))
        __paginator = loads(self.request.GET.get('paginator', "{}"))
        __ordening = loads(self.request.GET.get('ordening', "[]"))
        if pk:
            __filters.update({"pk": pk})
        __search = self.request.GET.get('search')
        # __filters.update({"user_id": self.request.user.id})
        self.get_sales(__filters, __paginator, __ordening, __search)

    def get_sales(self, filters={}, paginator={}, ordening=(), search=None):
        __array = []
        __rents = Sales.objects.select_related("user").filter(
            **filters).order_by(*ordening)
        for i in __rents:
            __dict = {
                "uuid": i.uuid,
                "user_email": i.user.email,
                "amount": i.amount,
                "date": str(i.create_at),
                "status": i.status,
                "status_name": "aprobada" if i.status else "anulada"
            }

            __array.append(__dict)

        if not filters.get('pk'):
            # import ipdb; ipdb.set_trace()
            self.paginator(__array, paginator)
            print(paginator)
        else:
            if not __array:
                self.result = {"result": "empty"}
                return
            self.result = __array[0]
