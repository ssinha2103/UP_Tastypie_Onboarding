from point_of_sale.models import *
from tastypie import fields
from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization


class UserResource(ModelResource):
    """Resource for User model (This model is DJANGO user model)."""
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        fields = ['username', 'email', 'password']
        authentication = Authentication()
        authorization = Authorization()
        include_resource_uri = False


class ProfileResource(ModelResource):
    """Resource for Profile model ."""
    user = fields.ToOneField(UserResource, 'user', full=True)

    class Meta:
        queryset = Profile.objects.all()
        resource_name = "profiles"
        authentication = Authentication()
        authorization = Authorization()
        include_resource_uri = False


class StoreResource(ModelResource):
    """Resource for Store model ."""
    merchant = fields.ToOneField('api.resources.ProfileResource', 'merchant', related_name='store_resource', full=True)

    class Meta:
        authentication = Authentication()
        authorization = Authorization()
        queryset = Store.objects.all()
        resource_name = 'stores'
        include_resource_uri = False
