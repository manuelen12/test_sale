# Stdlib imports
from json import loads, dumps
# Core Django imports
from django.contrib.auth import get_user_model
# from django.core.cache import cache
from rest_framework_jwt.settings import api_settings
from django.core.cache import cache
from datetime import datetime
from django.db.models import Q
from django.db.models import Count
# Imports from your apps
from common.utils import Base
from test_venta.sales.models import Sales
# from users.models import Peers
from common.utils import ThreadDef
from django.template.loader import render_to_string
from django.db.models import Prefetch
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()


class API(Base):
    def __init__(self, request):
        Base.__init__(self)
        self.request = request
        self.data = self.valid_data()
        self.error = {}
        self.result = []
        self.url_api = "http://"+self.request.META['HTTP_HOST']+"/api/v0"

    def valid_data(self):
        if self.request.method == "POST":
            __value = loads(dumps(self.request.data))
        if self.request.method == "GET":
            __value = loads(dumps(self.request.data))
        if self.request.method == "PUT":
            __value = loads(dumps(self.request.data))
        if self.request.method == "DELETE":
            __value = loads(dumps(self.request.data))
        print(__value)
        return __value

    def get_user(self, pk=None):
        __filters = loads(self.request.GET.get('filters', "{}"))
        __paginator = loads(self.request.GET.get('paginator', "{}"))
        __ordening = loads(self.request.GET.get('ordening', "[]"))
        if pk:
            __filters.update({"pk": pk})
        __search = self.request.GET.get('search')
        self.get_users(__filters, __paginator, __ordening, __search)

    def get_users(self, filters={}, paginator={}, ordening=(), search=None):
        __array = []
        # import ipdb; ipdb.set_trace()
        __x = Sales.objects.filter(status=True)
        __user = User.objects.prefetch_related(
                Prefetch(
                    "sales_user", queryset=__x, to_attr="sales_user2"),
            ).filter(
            **filters).order_by(*ordening)
        for i in __user:
            __dict2 = {
                "id": i.id,
                "first_name": i.first_name,
                "last_name": i.last_name,
                "address": i.address,
                "email": i.email,
                "status": i.status,
                "status_name": i.get_status_display(),
                "cant_sales": len(i.sales_user2),
                "amount_sales": 0
            }
            for i in i.sales_user2:
                __dict2['amount_sales'] += i.amount

            __array.append(__dict2)

        if not filters.get('pk'):
            self.paginator(__array, paginator)
            print(self.result)
        else:
            if not __array:
                self.result = {"result": "empty"}
                return
            self.result = __array[0]
        return __array

    def valid_register(self, kwargs):
        __valid = [
            'confirm_email', "first_name", "last_name", 'email',
            'password', 'confirm_password'
        ]
        if self.data.get('password') != self.data.get('confirm_password'):
            self._error_info("password", "password must be equals")
            return

        if not self._list_basic_info(kwargs, __valid):
            return
        if not self.list_only_string(self.data, ["first_name", "last_name"]):
            return
        if self.data.get('email') != self.data.get('confirm_email'):
            self._error_info("email", "email must be equals")
            return
        if not self._email(self.data.get('email')):
            return
        return True

    def register_user(self):
        if not self.valid_register(self.data):
            return
        try:
            user = User.objects.create_user(
                self.data.get('email'),
                self.data.get('email'),
                self.data.get('password',))
            __token = self.generator()
            cache.set(
                __token,
                user.id,
                60*60*60
            )
            print(cache.get(__token))
            user.first_name = self.data.get('first_name')
            user.last_name = self.data.get('last_name')
            user.address = self.data.get('address')
            user.status = True
            user.save()
        except Exception as e:
            self._error_info("error", str(e))
            return
        rendered = render_to_string(
            'confirmation_email.html', {
                "url": "http://"+self.
                request.META['HTTP_HOST']+"/api/v0/confirmation/"+__token})
        __start = ThreadDef(
            self.send_mail, *[self.data.get('email'),
                              "Confirmation Email", rendered])
        __start.start()
        self.result = {"result": {"user": "it send a email"}}

    def valid_forward_email(self, kwargs):
        __valid = [
            'email']
        if not self._list_basic_info(kwargs, __valid):
            return

        self.user = User.objects.filter(
            email=self.data.get('email')
        )
        if not self.user:
            self._error_info("email", "does not exist")
            return
        # if user.status:
        #     self._error_info("email", "dont have permission")
        #     return

    def forward_email(self):
        print("Post: " + str(self.request.data))
        if not self.valid_forward_email(self.data):
            # return
            self.data["email"]
        User.objects.filter(
            username=self.data.get('email')
        )

        __token = self.generator()
        print(__token)
        cache.set(
                __token,
                self.user[0].id,
                60*60*60
            )
        print(cache.get(__token))
        rendered = render_to_string(
            'confirmation_email.html', {
                "url": "http://"+self.
                request.META['HTTP_HOST']+"/api/v0/confirmation/"+__token})
        __start = ThreadDef(
            self.send_mail, *[self.data.get('email'),
                              "Confirmation Email", rendered])
        __start.start()
        self.result = {"result": {"user": "it send a email"}}

    def valid_change_confirmation(self, kwargs):
        __valid = ['token']
        if not self._list_basic_info(kwargs, __valid):
            return
        self.__id = cache.get(self.data.get('token'))
        if not self.__id:
            self._error_info('token', 'invalid token')
            return
        return True

    def change_confirmation(self, token):

        self.data['token'] = token
        print(token)
        # import ipdb; ipdb.set_trace()
        if not self.valid_change_confirmation(self.data):
            return
        __user = User.objects.get(id=self.__id)
        # x = __user
        # import ipdb; ipdb.set_trace()
        __user.status = 2
        __user.save()

    def valid_update(self, kwargs):
        __valid = [
            "first_name", "last_name",
        ]
        if not self._list_basic_info(kwargs, __valid):
            return
        if not self.list_only_string(self.data, ["first_name", "last_name"]):
            return
        return True

    def update_user(self):

        if not self._email(self.data.get('email')):
            return
        if not self.valid_update(self.data):
            return

        try:
            __u = User.objects.get(username=self.data.get('email'))
        except:
            self._error_info('email', 'it not exist')
            return

        __u.first_name = self.data.get('first_name')
        __u.last_name = self.data.get('last_name')
        __u.address = self.data.get('address')
        if self.data.get("password"):
            if self.data.get('password') != self.data.get('confirm_password'):
                self._error_info("password", "password must be equals")
                return
            __u.set_password(self.data.get("password"))
        __u.save()

        self.get_user(__u.pk)

    def deactivate_mail(self):
        if not self._email(self.data.get('email')):
            return
        try:
            __u = User.objects.get(username=self.data.get('email'))
        except:
            self._error_info('email', 'it not exist')
            return
        __u.status = 3
        __u.save()
        self.get_user(__u.pk)
