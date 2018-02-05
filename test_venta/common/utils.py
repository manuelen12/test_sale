# Stdlib imports
import hashlib
import random
import re
from datetime import datetime
from json import loads, dumps
import math
import string
from math import radians, cos, sin, asin, sqrt
# Core Django imports
from django.utils.translation import ugettext_lazy as _, activate
from django.core.files.storage import default_storage
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.mail import send_mail
# Third-party app imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework import routers
# Imports from your apps
from threading import Thread


class Pagin():

    def __init__(self, *args, **kwargs):
        # params
        self.result_data = []
        self.object = kwargs['object']
        self.page_results = kwargs['page_results']
        self.page_index = kwargs['page_index']
        self.pages = len(self.object) / float(self.page_results)
        if not self.pages.is_integer():
            self.pages = int(self.pages) + 1
        index_start = (self.page_index * self.page_results) - \
            (self.page_results)
        index_end = index_start + (self.page_results)
        self.result_data = self.object[index_start:index_end]

    def get(self):
        return {
            'data': self.result_data,
            'pages': int(self.pages),
            'page_index': self.page_index,
            'page_results': self.page_results,
            'total': len(self.object)
        }


class Base():
    def __init__(self, request=None):
        self.error = {}
        self.request = request
        self.status = 200
        self.zone_horaria = None
        self.date_now = None
        self.id_resource = None
        self.result = {}

    def valid_data(self):
        if self.request.method == "POST":
            __value = loads(dumps(self.request.data))
        if self.request.method == "GET":
            __value = loads(dumps(self.request.data))
        if self.request.method == "PUT":
            __value = loads(dumps(self.request.data))
        if self.request.method == "DELETE":
            __value = loads(dumps(self.request.data))
        return __value

    def _list_int_info(self, kwargs, lists):
        if not self._list_basic_info(kwargs, lists):
            return False
        for i in lists:
            if not kwargs.get(i):
                self._error_info(i, 'is required')
            self._is_number_int(kwargs[i], i)
        if self.error:
            return False
        return True

    def generator(self, size=5, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def update_or_create(self, objects, kwargs={}):
        try:
            obj = objects.objects.get(id=kwargs.get('id'))
            for key, value in kwargs.iteritems():
                setattr(obj, key, value)
                obj.save()
        except objects.DoesNotExist:
            obj = objects(**kwargs)
            obj.save()
        return obj

    def send_mail(self, email, subject, message):

        send_mail(
            subject, 'body of the message',
            settings.EMAIL_HOST_USER,
            [email], html_message=message)

    def valid_post(self):
        # import ipdb; ipdb.set_trace()
        if 'data' not in self.request.POST:
            self.status = 404
            self._data_error(self.error, "data", 'data is required')
            return

        self.data = loads(self.request.POST['data'])
        return True

    def valid_put(self):
        print(self.request.POST)
        if 'data' not in self.request.POST:
            self.status = 404
            self._data_error(self.error, "data", 'data is required')
            return

        self.data = loads(self.request.POST['data'])
        return True

    def _unicode_string(self, string):
        try:
            st = unicode(string)
            st = st.encode('unicode_escape')
            return st
        except:
            return string

    def _decode_string(self, string):
        try:
            return string.decode('unicode_escape')
        except:
            return string

    def language(self):
        if self.request.is_mobile:
            if 'HTTP_DAYLANG' in self.request.META:
                if str(self.request.META['HTTP_DAYLANG']) == 'en': trad = 'en'
                if str(self.request.META['HTTP_DAYLANG']) == 'es': trad = 'es'
            else:
                trad = 'en'
                try:
                    trad = str(self.request.user.user_profile.language.prefix)
                except: pass
            activate(trad)

    def _is_number_int(self, number, key, error=None, info=False, father=None, max_int=13, index=[], **kwargs):
        __errorT = error if not error is None else None
        try: number = int(number)
        except:
            if info:
                self._error_info(key, 'this is not a number', error=__errorT, father=father, index=index, **kwargs)
            else:
                self._data_error(__errorT, key, 'this is not a number')
            # if error:
            #     self._data_error(error, key, unicode(_("this is not a number")))
            # else:
            #     self._data_error(self.error, key, unicode(_("this is not a number")))
        else:
            __error = None
            if not max_int >= len(str(number)):
                __error = 'the number is very large'
            if __error:
                if info:
                    self._error_info(key, __error, error=__errorT, father=father, index=index, **kwargs)
                else:
                    self._data_error(__errorT, key, __error)
            else:
                return number

    def _is_number_float(self, number, key, error=None, info=False, father=None, max_int=13, max_decimal=5, index=[], **kwargs):
        __errorT = error if not error is None else None
        try: number = float(number)
        except:
            if info:
                self._error_info(key, 'is not a decimal number', error=__errorT, father=father, index=index, **kwargs)
            else:
                self._data_error(__errorT, key, 'is not a decimal number')
            # if error:
            #     self._data_error(error, key, unicode(_("is not a decimal number")))
            # else:
            #     self._data_error(self.error, key, unicode(_("is not a decimal number")))
        else:
            __error = None
            if (math.isinf(number) or math.isnan(number)):
                __error = 'is not a decimal number'
            if __error is None:
                __int = int(number)
                __decimal = number-int(number)
                if not max_int >= len(str(__int)):
                    __error = 'the number is very large'
                if max_decimal < len(str(__decimal)[2:]):
                    number = round(number, max_decimal)

            if __error:
                if info:
                    self._error_info(key, __error, error=__errorT, father=father, index=index, **kwargs)
                else:
                    self._data_error(__errorT, key, __error)
            else:
                return number

    def _basic_info(self, key, objects, keyInfo, valueInfo="is required", error=None, info=False, father=None, index=[], **kwargs):
        if self._basic_required(key, objects):
            return True
        else:
            __errorT = error if not error is None else None
            if info:
                self._error_info(keyInfo, valueInfo, error=__errorT, father=father, index=index, **kwargs)
            else:
                self._data_error(__errorT, keyInfo, valueInfo)
            # if error: self._data_error(error, keyInfo, valueInfo)
            # else: self._data_error(self.error, keyInfo, valueInfo)

    def _basic_required(self, key, objects):
        if self._data_in_objects(key, objects):
            if self._data_existente(key, objects):
                return True

    def _validate_json(self, data, key, error=None, info=False, father=None, index=[], **kwargs):
        try:
            return loads(data)
        except:
            # self._data_error(key=key)
            __errorT = error if not error is None else None
            if info:
                self._error_info(key, error=__errorT, father=father, index=index, **kwargs)
            else:
                self._data_error(__errorT, key)

    def _validate_models(self, element, objecto, models, valueInfo, owner=False):
        if owner:
            if element:
                return self.__validate_models(element, models, valueInfo)
        else:
            if self._basic_info(element, objecto, valueInfo):
                return self.__validate_models(objecto[element], models, valueInfo)

    def __validate_models(self, data, models, valueInfo):
        try:
            if isinstance(data, models):
                return data
            elif isinstance(data, str) or isinstance(data, int) or isinstance(data, unicode):
                return models.objects.get(pk=data)
            else:
                if isinstance(data[0], models):
                    return data[0]
        except:
            self._data_error(key=valueInfo)

    def _data_in_objects(self, key, objects):
        if key in objects:
            return True

    def _get_time(self, date):
        # from django.utils import translation
        __p = date.strftime('%p').lower()[:-1]
        __I = date.strftime('%I')
        __M = date.strftime('%M')
        # if translation.get_language() == "es":
        return '%s:%s%s' % (__I, __M, __p)
        # else:
            # return '%s:%s%s'%(b,d,Y,I,M,p)

    # def _validate_date(self, objects, key, tz=None, web=True, error=None, info=False, father=None, index=[], **kwargs):
    #     try:
    #         if web is 1:
    #             __date = datetime.strptime(str(objects)+'m', '%d-%m-%Y %I:%M%p')
    #         elif web is True:
    #             __date = datetime.strptime(objects, '%d-%m-%Y %I:%M %p')
    #         else:
    #             __date = datetime.strptime(objects, '%Y-%m-%d %H:%M:%S')
    #         if tz:
    #             __date = self._localize(__date)
    #     except:
    #         __errorT = error if not error is None else None
    #         if info:
    #             self._error_info(key, error=__errorT, father=father, index=index, **kwargs)
    #         else:
    #             self._data_error(__errorT, key)
    #     else:
    #         return __date

    def _data_existente(self, key, objects):
        if isinstance(objects[key], list) or isinstance(objects[key], dict):
            if objects[key]: return True
        else:
            if not objects[key] is None:
                # if isinstance(objects[key], int) or isinstance(objects[key], float):
                    # if objects[key]: return True
                # else:
                try:
                    if len(str(objects[key])): return True
                except:
                    if len(objects[key]): return True

    def _phone(self, phone, country=None):
        # if re.findall(r"^\+\d{1,4}-\d{9,11}$", phone):
        if re.findall(r"^\+\d{1,4}(-\d{1,4})?-\(\d{3}\)[ ]\d{3}-\d{4}$", phone):
            # if country:
            #     if re.findall(r'^'+country, phone):
            #         pass
            #     else: return
            return True
        else:
            self._error_info("phone", 'format is incorrect')
            return

    def _phone_mobile(self, phone, country=None):
        # if re.findall(r"^\+\d{1,4}-\d{9,11}$", phone):
        if re.findall(r"^\+\d{1,4}(-\d{1,4})?-\d{9,11}$", phone):
            return True
        else:
            self._error_info("phone", 'format is incorrect')
            return

    def _data_error(self, error=None, key=None, value="data not valid"):
        if isinstance(value, str):
            value = str(_(value))

        if error is None:
            if key in self.error:
                if isinstance(self.error[key], list):
                    self.error[key].append(value)
                else:
                    self.error[key] = [self.error[key], value]
            else: self.error.update({key: value})
        else:
            if key in error:
                if isinstance(error[key], list):
                    error[key].append(value)
                else:
                    error[key] = [error[key], value]
            else: error.update({key: value})

    def _error_info(self, key, value='data not valid', father=None, error=None, index=[], status=404, **kwargs):
        self.status = status
        if  isinstance(value, str):
            value = str(_(value))

        if  isinstance(value, str):
            key = str(_(key)).title()

        if not error is None:
            if not isinstance(error, list): error = []
            __errorT = error
        else:
            if not isinstance(self.error, list): self.error = []
            __errorT = self.error

        __dic = {'field': key, 'error': value}
        if kwargs:
            __dic.update(kwargs)
        if father:
            __t = []
            if isinstance(father, list):
                __loop = 0
                for i in range(len(father)):
                    __y = filter(lambda x: str(x['field']) == str(father[i]), __t[0]['error'] if __t else __errorT)
                    if __y:
                        if __t: __t = __t[0]['error']
                        else: __t = __y
                    else:
                        __dict = {'field': father[i], 'error': []}
                        if __loop < len(index):
                            if not index[__loop] == '':
                                __dict.update({'index': index[__loop]})
                        if __t:
                            __t[0]['error'].append(__dict)
                        else:
                            __errorT.append(__dict)
                        __t = filter(lambda x: x['field'] == father[i], __errorT if not __t else __t[0]['error'])
                    __loop += 1
                if __loop == len(index)-1:
                    if not index[__loop] == '':
                        __dic.update({'index': index[__loop]})
            else:
                __t = filter(lambda x: x['field'] == father, __errorT)
                if not __t:
                    __dict = {'field': father, 'error': [__dic]}
                    if index:
                        if not index[0] == '':
                            __dict.update({'index': index[0]})
                    __errorT.append(__dict)

            if __t:
                __t[0]['error'].append(__dic)

        else:
            __errorT.append(__dic)

    # def _images(self, img, key, info=None, father=None, index=[], **kwargs):
        data = []
        error = False
        # if not isinstance(img, list):
        #     img = [img]
        # if img:
        #     for i in img:
        #         try: i = int(i)
        #         except:
        #             x_t = urllib2.urlopen(i)
        #             __ext = dict(x_t.info())['content-type']
        #             if not __ext in ['image/jpeg', 'image/png']:
        #                 error = True
        #                 break
        #         data.append(i)
        if error:
            # self._data_error(self.error, key, unicode(_("format not valid")))
            # __errorT = error if not error is None else self.error
            if info:
                self._error_info(key, 'format not valid', father=father, index=index, **kwargs)
            else:
                self._data_error(key=key, value='format not valid')
        else:
            return data

    def _list_basic_info(self, data, lists, name_dict=None):
        if not isinstance(data, dict):
            self._data_error(key=name_dict, value='Must be a dict')
            return False

        __valid = True
        for i in lists:
            if not self._basic_info(i, data, i, info=True, father=name_dict):
                __valid = False
        return __valid

    def _email(self, email):
        # import ipdb; ipdb.set_trace()
        if re.search(r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,3})$", email):
            return True
        else:
            self._error_info("email", 'format is incorrect')
            return

    def _len_min_string(self, min_string, string, key, error=None, info=False, father=None, index=[], **kwargs):
        if len(string) < min_string:
            __errorT = error if not error is None else None
            if info:
                self._error_info(key, 'minimum characters not valid', error=__errorT, father=father, index=index, **kwargs)
            else:
                self._data_error(__errorT, key, 'minimum characters not valid')
            # if error:
            #     self._data_error(error, key, unicode(_("minimum characters not valid")))
            # else:
            #     self._data_error(self.error, key, unicode(_("minimum characters not valid")))
        else:
            return True

    def _ifinerror(self, key):
        if isinstance(key, list):
        # if __t and isinstance(__t[0]['error'], list):
        #     __t = filter(lambda x: x["field"] == father, __t[0]['error'])
            __t = []
            for i in key:
                __t = filter(lambda x: x["field"] == i, __t[0]['error'] if __t else self.error)
                if not __t: break
            # for i in key:
            #     __t = filter(lambda x: x["field"] == key, self.error)
            #     if not __t: break
        else:

            __t = filter(lambda x: x["field"] == key, self.error)
        return __t

    def _validate_image_with_main(self, current, new_data, key, error=None, info=False, father=None, index=[], **kwargs):
        __errorT = error if not error is None else None
        __error_messages = ''
        __add_image = []
        __delete_image = []
        __change_image = None
        __inactive_image = None
        __sent_main = False
        __required_main = False
        try:
            for i in new_data:
                try: __init = int(i['path'])
                except:
                    __main = False
                    if 'main' in i and not __sent_main:
                        try:
                            if int(i['main']):
                                __main = True
                                __sent_main = True
                                __inactive_image = filter(lambda x: x['main'], current)[0]['id']
                        except: pass
                    __add_image.append({'path': i['path'], 'niarmi': 1, 'main': __main})
                else:
                    __t = filter(lambda x: x['media__resource'] == __init, current)
                    if __t:
                        try:
                            if int(i['delete']):
                                if __t[0]['main']:
                                    __required_main = True
                                __delete_image.append(__t[0]['id'])
                        except: pass
                        if not __sent_main:
                            try:
                                if int(i['main']):
                                    __sent_main = True
                                    __id_del = filter(lambda x: x['main'], current)[0]['id']
                                    if not __id_del == __t[0]['id']:
                                        __inactive_image = filter(lambda x: x['main'], current)[0]['id']
                                        __change_image = __t[0]['id']
                            except: pass
                    else:
                        __error_messages = 'the image not belong a this image'
                        break
        except:
            __error_messages = 'data invalid'

        if not __error_messages:
            __len_image = len(current)
            if __len_image + len(__add_image) - len(__delete_image) < 1:
                __error_messages = 'Must have at least one image'
            elif __len_image + len(__add_image) - len(__delete_image) > 10:
                __error_messages = 'You can only have a maximum of ten images'
            else:
                if __required_main:
                    if not __sent_main:
                        if __len_image + len(__add_image) - len(__delete_image) == 1:
                            if len(__add_image) == 1:
                                __add_image[0].update({'main': True})
                            else:
                                __t = filter(lambda x: not x['id'] in __delete_image, current)
                                if len(__t) == 1:
                                    __t[0].update({'main': True})
                                    __change_image = __t[0]['id']
                                else:
                                    __error_messages = 'You must sent main image'
                        else:
                            __error_messages = 'You must sent main image'
                else:
                    if not __len_image and not __sent_main:
                        if len(__add_image) > 1:
                            __error_messages = 'You must sent main image'
                        else:
                            __add_image[0].update({'main': True})
                if not __error_messages:
                    if __delete_image and __inactive_image:
                        if __inactive_image in __delete_image:
                            __inactive_image = None
                    __dic = {
                        'add': __add_image,
                        'delete': __delete_image,
                        'update': __change_image,
                        'inactive': __inactive_image
                    }
                    return __dic
        if info:
            self._error_info(key, __error_messages, error=__errorT, father=father, index=index, **kwargs)
        else:
            self._data_error(__errorT, key, __error_messages)

    def _ifnoterror(self, key, value=None):
        __dic = {}
        if value:
            __dic.update({'value': value})
        __t = self._ifinerror(key)
        if not __t:
            self._error_info(key, **__dic)

    def get(self):
        if self.error:
            print ("error", dumps(self.error))
        if self.error:
            return {"status": self.status, "get": {"valid": False, "error": self.error}}
        else:
            __out = {"valid": True}
            if self.id_resource: __out.update({"id": self.id_resource})
            if self.result: __out.update(self.result)
            if not self.date_now: __date = datetime.now()
            else: __date = self.date_now
            __out.update({
                "date": {
                    "movil": __date.strftime('%Y-%m-%d %H:%M:%S'),
                    "web": __date.strftime('%d/%m/%Y %I:%M %p')
                }
            })
            return {"status": self.status, "get": __out}

    def _validate_time(self, time, father):

        if re.findall(r"^[0-9]{2}:[0-9]{2}:[0-9]{2}$", time):
            return True
        else:
            self._error_info("time", "the format must be HH:MM:SS",
                             error=None, father=father)
            return

    def _phone1(self, phone, kwargs, country_o):
        if not 'phone_code' in kwargs and not 'id' in kwargs:
            self._error_info(key='phone', value='phone_code or id is required')
            return
        try:
            __valid_phone = country_o.objects.get(**kwargs)
        except:
            self._error_info(key='phone', value='invalid')
            return
        if re.findall(r""+__valid_phone.regex_phone, phone):
            return True
        else:
            self._error_info(key='phone1', value='format is bad')
            return

    def export_attr(self, Model, kwargs):
        # import ipdb; ipdb.set_trace()
        __model_attr = [i.name+"_id" if i.many_to_one else i.name for i in Model._meta.get_fields()]
        print (Model._meta.get_fields())
        __values = {}

        for k, v in kwargs.items():
            if k in __model_attr:
                __values.update({str(k): v})
        self.values = __values

    def paginator(self, query, params):
        try:
            paginator = params
        except:
            paginator = {}

        if paginator:
            try:
                __page = int(paginator['page'])
            except:
                __page = 1

            try:
                __page_results = int(paginator['page_results'])
            except:
                __page_results = 8

            P = Pagin(
                object=query,
                page_results=__page_results,
                page_index=__page
            )
            self.result = {
                'data': P.get()['data'],
                'page_results': __page_results,
                'page_index': __page,
                'total_pages':  P.get()['pages'],
                'total_results': len(query)
            }
        else:
            self.result = query

    def list_only_string(self, kwargs, lists):
        for i in lists:
            if re.search(r"[0-9]", kwargs.get(i)):
                self._error_info(i, 'cant have numbers')
        if self.error:
            return False
        # print(kwargs)
        return True

    def renew(self, token, access, newkey):
        __value = self.decrypt(token, access)
        __env = self.encrypt(newkey, __value)
        return __env

    def distance_two_point(self, point1, point2, miles=False):
        # import ipdb; ipdb.set_trace()
        # print(point1)
        lat1, lng1 = point1
        lat2, lng2 = point2
        AVG_EARTH_RADIUS = 6371  # in km
        # convert all latitudes/longitudes from decimal degrees to radians
        lat1, lng1, lat2, lng2 = map(radians, (lat1, lng1, lat2, lng2))

        # calculate haversine
        lat = lat2 - lat1
        lng = lng2 - lng1
        d = sin(lat * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(lng * 0.5) ** 2
        h = 2 * AVG_EARTH_RADIUS * asin(sqrt(d))
        if miles:
            return h * 1000  # in miles
        else:
            return h * 1000  # in kilometers

    # def geoip2(self, ip):
    #     __reader = geoip2.database.Reader(settings.GEOLOCATION_PLACE)
    #     __status = True
    #     __message = ""
    #     # import ipdb; ipdb.set_trace()
    #     try:
    #         __city = __reader.city(ip)
    #     except:
    #         __status = False
    #         __city = __reader.city("186.92.243.159")

    #     self.geo_info = {
    #         "country": __city.country.name,
    #         "state": __city.subdivisions.most_specific.name,
    #         "city": __city.city.name,
    #         "time_zone": __city.location.time_zone,
    #         "latitude": __city.location.latitude,
    #         "longitude": __city.location.longitude,
    #         "status": __status,
    #         "mensaje": __message
    #     }

    def remove_space_string(self, string):
        x = "".join(string.split())
        return x

    def daterange(self, start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)


def generate_random_token(extra=None, hash_func=hashlib.sha256):
    if extra is None:
        extra = []
    bits = extra + str(random.SystemRandom().getrandbits(512))
    return hash_func("".join(bits).encode("utf-8")).hexdigest()

CODES = {
    "100": status.HTTP_100_CONTINUE,
    "101": status.HTTP_101_SWITCHING_PROTOCOLS,
    "200": status.HTTP_200_OK,
    "201": status.HTTP_201_CREATED,
    "202": status.HTTP_202_ACCEPTED,
    "203": status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
    "204": status.HTTP_204_NO_CONTENT,
    "205": status.HTTP_205_RESET_CONTENT,
    "206": status.HTTP_206_PARTIAL_CONTENT,
    "207": status.HTTP_207_MULTI_STATUS,
    "300": status.HTTP_300_MULTIPLE_CHOICES,
    "301": status.HTTP_301_MOVED_PERMANENTLY,
    "302": status.HTTP_302_FOUND,
    "303": status.HTTP_303_SEE_OTHER,
    "304": status.HTTP_304_NOT_MODIFIED,
    "305": status.HTTP_305_USE_PROXY,
    "306": status.HTTP_306_RESERVED,
    "307": status.HTTP_307_TEMPORARY_REDIRECT,
    "400": status.HTTP_400_BAD_REQUEST,
    "401": status.HTTP_401_UNAUTHORIZED,
    "402": status.HTTP_402_PAYMENT_REQUIRED,
    "403": status.HTTP_403_FORBIDDEN,
    "404": status.HTTP_404_NOT_FOUND,
    "405": status.HTTP_405_METHOD_NOT_ALLOWED,
    "406": status.HTTP_406_NOT_ACCEPTABLE,
    "407": status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED,
    "408": status.HTTP_408_REQUEST_TIMEOUT,
    "409": status.HTTP_409_CONFLICT,
    "410": status.HTTP_410_GONE,
    "411": status.HTTP_411_LENGTH_REQUIRED,
    "412": status.HTTP_412_PRECONDITION_FAILED,
    "413": status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    "414": status.HTTP_414_REQUEST_URI_TOO_LONG,
    "415": status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    "416": status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
    "417": status.HTTP_417_EXPECTATION_FAILED,
    "422": status.HTTP_422_UNPROCESSABLE_ENTITY,
    "423": status.HTTP_423_LOCKED,
    "424": status.HTTP_424_FAILED_DEPENDENCY,
    "428": status.HTTP_428_PRECONDITION_REQUIRED,
    "429": status.HTTP_429_TOO_MANY_REQUESTS,
    "431": status.HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE,
    "451": status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
    "500": status.HTTP_500_INTERNAL_SERVER_ERROR,
    "501": status.HTTP_501_NOT_IMPLEMENTED,
    "502": status.HTTP_502_BAD_GATEWAY,
    "503": status.HTTP_503_SERVICE_UNAVAILABLE,
    "504": status.HTTP_504_GATEWAY_TIMEOUT,
    "505": status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED,
    "507": status.HTTP_507_INSUFFICIENT_STORAGE,
    "511": status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED,
}


def default_responses(code=int, data=None):

    if data or isinstance(data, list) or isinstance(data, dict):
        if code == 200:
            return Response(data, status=CODES[str(code)])
        else:
            return Response({"raise": data}, status=CODES[str(code)])
    else:
        return Response(status=CODES[str(code)])


class DefaultRouter(routers.DefaultRouter):
    """
    Extends `DefaultRouter` class to add a method for extending url routes from another router.
    """
    def extend(self, router):
        """
        Extend the routes with url routes of the passed in router.

        Args:
             router: SimpleRouter instance containing route definitions.
        """
        self.registry.extend(router.registry)


class UploadFile(Base):
    def __init__(self, request):
        self.result = {}
        self.error = {}
        self.status = 200
        self.request = request
        self.url_api = settings.HTTP+self.request.META['HTTP_HOST']+"/api/v0/"

    def upload(self):
        # import ipdb; ipdb.set_trace()
        if not self.request.FILES.get('file'):
            self._error_info('file', "it is not exists")
            return
        __files = self.request.FILES['file']
        __files = default_storage.save(
            'tmp_media/' + __files.name,
            ContentFile(__files.read()))
        self.result['url'] = self.url_api+__files


class ThreadDef(Thread):

    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        Thread.__init__(self)

    def run(self):
        self.func(*self.args, **self.kwargs)
