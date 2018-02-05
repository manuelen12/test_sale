# Stdlib imports
# Core Django imports
from django.conf.urls import url, include
# Third-party app imports
from rest_framework import routers
# Imports from your apps
from test_venta.sales.v0.views import (RentViewSets)

router = routers.DefaultRouter()

router.register(r'sale', RentViewSets, base_name='sale')
# urlpatterns = [
#     url(r'^', include(router.urls)),
# ]
