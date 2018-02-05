# from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
# Imports from your apps
from test_venta.common.utils import default_responses
from .api import Controller
from .serializers import (RentSerializer)


class RentViewSets(viewsets.ViewSet):

    serializer_class = RentSerializer
    """
    SECTION OF PLANS
    """
    def create(self, request, *args, **kwargs):
        serializer = Controller(request)
        serializer.create_sale()

        if serializer.error:
            return default_responses(404, serializer.error)
        print(serializer.result)
        return default_responses(200, serializer.result)

    def list(self, request, *args, **kwargs):
        serializer = Controller(request)
        serializer.get_sale()
        if serializer.error:
            print(serializer.error)
            return default_responses(400, serializer.error)

        return default_responses(200, serializer.result)

    def retrieve(self, request, pk, *args, **kwargs):
        serializer = Controller(request)
        serializer.get_sale(pk)
        if serializer.error:
            print(serializer.error)
            return default_responses(400, serializer.error)

        return default_responses(200, serializer.result)
    # def update(self, request, pk, *args, **kwargs):
    #     serializer = Controller(request)
    #     serializer.update_plan(pk)
    #     if serializer.error:
    #         print(serializer.error)
    #         return default_responses(404, serializer.error)

    #     return default_responses(200, serializer.result)

    # def destroy(self, request, pk, *args, **kwargs):
    #     serializer = Controller(request)
    #     serializer.delete_plan(pk)
    #     if serializer.error:
    #         return default_responses(404, serializer.error)

    #     return default_responses(200, serializer.result)
