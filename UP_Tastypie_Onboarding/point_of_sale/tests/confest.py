import pytest
from point_of_sale.models import Profile, Store, Item
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def merchant_data():
    merchant = User.objects.create_user(username="merchant", email="merchant@gmail.com", password="merchant")
    profile = Profile.objects.create(user=merchant, name="Merchant_User", role=1)
    return profile


@pytest.fixture
def consumer_data():
    consumer = User.objects.create_user(username="consumer", email="consumer@gmail.com", password="consumer")
    profile = Profile.objects.create(user=consumer, name="consumer_User", role=2)
    return profile


@pytest.fixture
def store_data(merchant_data):
    store = Store.objects.create(name="WhiteField Outlet", address="WhiteField", lat=13, lng=13, merchant=merchant_data)
    return store


@pytest.fixture
def item_data(store_data):
    item = Item.objects.create(name="Dosa", price=120, description="Sambhar Dosa", stores=['/api/v1/stores/1/'])
    return item

