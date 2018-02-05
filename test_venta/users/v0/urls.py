"""configuration_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# from django.conf.urls import url, include
from rest_framework import routers
from .views import (
                    DeactivateViews,
                    UserViews,
                    ConfirmationViewSet,
                    UpdateUserViews
                    )
# from rest_framework.urlpatterns import format_suffix_patterns

router = routers.SimpleRouter()
router.register(r'user', UserViews, base_name='user')
router.register(r'deactivate', DeactivateViews, base_name='deactivate')
router.register(r'confirmation', ConfirmationViewSet, base_name='confirmation')
router.register(r'update_user', UpdateUserViews, base_name='update_user')
