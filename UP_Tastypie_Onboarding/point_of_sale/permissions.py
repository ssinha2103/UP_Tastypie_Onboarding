from abc import ABC

from django.http import HttpResponse
from tastypie.exceptions import Unauthorized

from point_of_sale.models import *
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication


class MerchantStoreAuthorization(Authorization, ABC):
    """Custom Authorization model for generating Merchant Authorization"""

    def read_list(self, object_list, bundle):
        """Overriding read_list method to filter out object_list based on user"""
        profile = Profile.objects.get(user=bundle.request.user)
        if profile.role == 1:
            return object_list.filter(merchant__user=bundle.request.user)
        else:
            # raise Unauthorized("No Access")
            return HttpResponse('Unauthorized', status=401)

    def create_detail(self, object_list, bundle):
        """Overriding create_detail method to provide write access of stores to only merchants"""
        profile = Profile.objects.get(user=bundle.request.user)
        if profile.role == 1:
            return True
        else:
            # raise Unauthorized("No Access")
            return False


class MerchantItemAuthorization(Authorization, ABC):
    def read_list(self, object_list, bundle):
        """Overriding read_list method to filter out object_list based on profile"""
        profile = Profile.objects.get(user=bundle.request.user)
        if profile.role == 1:
            return object_list.filter(stores__merchant=profile)
        else:
            raise Unauthorized("No Access")


class MerchantOrderResourceAuthorization(Authorization, ABC):
    """Custom Authorization model for generating Merchant Order Authorization"""

    def read_list(self, object_list, bundle):
        """Overriding read_list method to filter out object_list based on user"""
        profile = Profile.objects.get(user=bundle.request.user)
        if profile.role == 1:
            return object_list.filter(merchant__user=bundle.request.user)
        else:
            # raise Unauthorized("No Access")
            return HttpResponse('Unauthorized', status=401)


class ConsumerOrderResourceAuthorization(Authorization, ABC):
    """Custom Authorization model for generating Consumer Order Authorization"""

    def read_list(self, object_list, bundle):
        """Overriding read_list method to filter out object_list based on user"""
        profile = Profile.objects.get(user=bundle.request.user)
        if profile.role == 2:
            return object_list.filter(user=bundle.request.user)
        else:
            # raise Unauthorized("No Access")
            return HttpResponse('Unauthorized', status=401)


class PassAuthentication(Authentication):
    """Dummy Authentication class which allows some services to all users (logged-in/logged-out)"""
    def is_authenticated(self, request, **kwargs):
        return True


class PassAuthorization(Authorization, ABC):
    """Dummy Authorization class which allows some services to all users (logged-in/logged-out)"""
    def read_list(self, object_list, bundle):
        return object_list.filter()
