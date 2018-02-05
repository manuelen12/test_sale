
# Stdlib imports
# Core Django imports
# Third-party app imports
from rest_framework import serializers
# from django import forms
# Imports from your apps
from django.contrib.auth import get_user_model
User = get_user_model()


class USerSerializer(serializers.Serializer):

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    address = serializers.CharField()
    email = serializers.EmailField()
    confirm_email = serializers.EmailField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()


class UpdateUSerSerializer(serializers.Serializer):

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    address = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()


class ResendSerializers(serializers.Serializer):

    email = serializers.EmailField()
