# Stdlib imports

# Core Django imports
# Third-party app imports
from rest_framework import viewsets
from rest_framework import permissions
from django.shortcuts import redirect
# Imports from your apps
from common.utils import default_responses
from .api import API
from .serializers import (
    USerSerializer,
    ResendSerializers,
    UpdateUSerSerializer
)
# from gaver.users.models import (User)
from django.contrib.auth import get_user_model
# from rest_framework.viewsets import GenericViewSet
User = get_user_model()


class UserViews(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)
    """
        POST To Login with some user
        GET All local files
        GET /{id}/ get just the information of a file
        PUT /{id}/ Change the privileges of the file or share a file
        DELETE /{id}/ DELETE a file
    """
    serializer_class = USerSerializer

    def create(self, request, format=None, *args, **kwargs):
        serializer = API(request)
        serializer.register_user()
        if serializer.error:
            print(serializer.error)
            return default_responses(400, serializer.error)

        return default_responses(200, serializer.result)

    def list(self, request, *args, **kwargs):
        serializer = API(request)
        serializer.get_user()
        if serializer.error:
            print(serializer.error)
            return default_responses(400, serializer.error)

        return default_responses(200, serializer.result)


class UpdateUserViews(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)
    """
        POST To Login with some user
        GET All local files
        GET /{id}/ get just the information of a file
        PUT /{id}/ Change the privileges of the file or share a file
        DELETE /{id}/ DELETE a file
    """
    serializer_class = UpdateUSerSerializer

    def create(self, request, format=None, *args, **kwargs):
        serializer = API(request)
        serializer.update_user()
        if serializer.error:
            print(serializer.error)
            return default_responses(400, serializer.error)

        return default_responses(200, serializer.result)

    def list(self, request, *args, **kwargs):
        serializer = API(request)
        serializer.get_user()
        if serializer.error:
            print(serializer.error)
            return default_responses(400, serializer.error)

        return default_responses(200, serializer.result)


class DeactivateViews(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    serializer_class = ResendSerializers

    def create(self, request, format=None, *args, **kwargs):
        serializer = API(request)
        serializer.deactivate_mail()
        if serializer.error:
            print(serializer.error)
            return default_responses(400, serializer.error)

        return default_responses(200, serializer.result)


class ConfirmationViewSet(viewsets.GenericViewSet):

    permission_classes = (permissions.AllowAny,)

    def retrieve(self, request, pk, *args, **kwargs):
        serializer = API(request)
        serializer.change_confirmation(pk)
        if serializer.error:
            print(serializer.error)
            return default_responses(404, serializer.error)
        return default_responses(200, serializer.result)
