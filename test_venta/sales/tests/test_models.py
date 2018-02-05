import pytest
from mixer.backend.django import mixer
from rental.rents.models import Bike, PriceByFrecuency, Rentals
pytestmask = pytest.mark.django_db

@pytest.mark.django_db
class TestRentals:
    def test_bike_model(self):
        bike = mixer.blend(Bike)
        assert bike.pk == 1, 'should create a Bike instance'

        assert str(bike)

    def test_rent_model(self):
        rent = mixer.blend(Rentals)
        assert rent.pk == 1, 'should create a Rents instance'

        assert str(rent) == rent.user.username

    def test_price_by_frecuency_model(self):
        price_by_frecuency = mixer.blend(PriceByFrecuency)
        assert price_by_frecuency.pk == 1, 'PriceByFrecuency instance'

        assert str(price_by_frecuency) == price_by_frecuency.get_frequently_display()
