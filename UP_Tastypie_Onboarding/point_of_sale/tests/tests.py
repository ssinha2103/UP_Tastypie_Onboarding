import pytest
from tastypie.test import TestApiClient as ApiClient
import pdb
from .confest import *
import base64

client = ApiClient()
User = get_user_model()


@pytest.mark.django_db
def test_merchant_registration():
    """Merchant Registration Test Case"""
    # import pdb; pdb.set_trace()
    payload = {
        'name': 'Merchant',
        'role': 1,
        'user': {
            'email': 'merchant@gmail.com',
            'password': 'merchant',
            'username': 'merchant'
        }
    }
    response = client.post("/api/v1/profiles/", data=payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_merchant_login(merchant_data):
    """Merchant Login Test Case"""
    # pdb.set_trace()
    payload = {
        "username": "merchant",
        "password": "merchant"
    }
    response = client.post("/api/v1/user/login/", data=payload)
    assert response.status_code == 200


# Stores Creation EndPoint Test Case
@pytest.mark.django_db
def test_store_creation_api_endpoint(merchant_data):
    """Store Creation Test Case"""
    # import pdb; pdb.set_trace()
    payload = {
        "name": "WhiteField Outlet",
        "address": "WhiteField",
        "lat": 13,
        "lng": 13,
        "merchant": "/api/v1/profiles/1/"
    }
    req_send = client.post("/api/v1/stores/", data=payload,
                           **{'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(b'merchant:merchant').decode("ascii")})
    assert req_send.status_code == 201


# Items Creation Endpoint Test Case
@pytest.mark.django_db
def test_item_creation_api_endpoint(store_data):
    """Item Creation Test Case"""
    # import pdb; pdb.set_trace()
    payload = {
        "name": "Dosa",
        "price": 120,
        "description": "Sambhar Dosa",
        "stores": ["/api/v1/stores/1/"]
    }
    req_send = client.post("/api/v1/items/", data=payload,
                           **{'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(b'merchant:merchant').decode("ascii")})
    assert req_send.status_code == 201


# consumer Login & Registration Test Case
@pytest.mark.django_db
def test_consumer_registration():
    """Consumer Registration Test Case"""
    payload = payload = {
        'name': 'Consumer',
        'role': 1,
        'user': {
            'email': 'consumer@gmail.com',
            'password': 'consumer',
            'username': 'consumer'
        }
    }
    response = client.post("/api/v1/profiles/", data=payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_consumer_login(consumer_data):
    """Consumer Login Test Case"""
    payload = {
        "username": "consumer",
        "password": "consumer"
    }
    response = client.post("/api/v1/user/login/", data=payload)
    assert response.status_code == 200


@pytest.mark.django_db
def test_place_order_api_endpoints(merchant_data, store_data, item_data, consumer_data):
    """Test Place Order Endpoints"""
    # import pdb; pdb.set_trace()
    payload = {
        "user": "/api/v1/users/2/",
        "store": "/api/v1/stores/1/",
        "merchant": "/api/v1/profiles/1/",
        "items": ["/api/v1/items/1/"]
    }
    req_send = client.post("/api/v1/place_order/", data=payload,
                           **{'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(b'consumer:consumer').decode("ascii")})

    assert req_send.status_code == 201
    items_present = set(Item.objects.all().values_list('name', flat=True))
    assert "Dosa" in items_present
