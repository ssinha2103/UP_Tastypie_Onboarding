from point_of_sale.models import *
from tastypie import fields
from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication, Authentication
from tastypie.authorization import Authorization
from point_of_sale.permissions import *
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.conf.urls import url


class UserResource(ModelResource):
    """Resource for User model (This model is DJANGO user model)."""

    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        fields = ['username', 'email', 'password']
        authentication = PassAuthentication()
        authorization = PassAuthorization()
        include_resource_uri = False


class ProfileResource(ModelResource):
    """Resource for Profile model . Helps in fetching and creating new users + profiles"""
    user = fields.ToOneField(UserResource, 'user', full=False)

    class Meta:
        queryset = Profile.objects.all()
        resource_name = "profiles"
        authentication = PassAuthentication()
        authorization = PassAuthorization()
        include_resource_uri = False

    def obj_create(self, bundle, **kwargs):
        """Overrides the obj_create method of ModelResource"""
        user_data = bundle.data.pop("user")
        user = User.objects.create(
            username=user_data["username"],
            email=user_data["email"],
        )
        user.set_password(user_data["password"])
        user.save()
        profile = Profile.objects.create(user=user, role=bundle.data["role"], name=bundle.data["name"])
        bundle.obj = self._meta.object_class()
        return profile

    def prepend_urls(self):
        """Appending urls after profile resource for login and logout."""
        return [
            url(r"^user/login/$", self.wrap_view('login'), name="api_login"),
            url(r"^user/logout/$", self.wrap_view('logout'), name='api_logout'),
        ]

    def login(self, request, **kwargs):
        """Login function for the profile resource"""
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))

        username = data.get('username', '')
        password = data.get('password', '')
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        print(user)
        if user:
            if user.is_active:
                login(request, user)
                return self.create_response(request, {
                    'success': True
                })
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                }, HttpForbidden)
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect',
            }, HttpUnauthorized)

    def logout(self, request, **kwargs):
        """Logout function for the profile resource"""
        self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated:
            logout(request)
            return self.create_response(request, {'success': True})
        else:
            return self.create_response(request, {'success': False}, HttpUnauthorized)


class StoreResource(ModelResource):
    """Resource for Store model . Helps in fetching and creating new Stores"""
    merchant = fields.ToOneField('api.resources.ProfileResource', 'merchant', related_name='store_resource', full=False)

    class Meta:
        authentication = BasicAuthentication()
        authorization = MerchantStoreAuthorization()
        queryset = Store.objects.all()
        resource_name = 'stores'
        include_resource_uri = False

    def get_object_list(self, request):
        """Overrides the get_object_list method of ModelResource"""
        return super(StoreResource, self).get_object_list(request).filter(merchant__user=request.user)


class ItemResource(ModelResource):
    """Resource for Item model. Helps in fetching and creating new Items."""
    stores = fields.ToManyField('api.resources.StoreResource', 'stores', related_name='item_resource', full=False)

    class Meta:
        authentication = BasicAuthentication()
        authorization = MerchantItemAuthorization()
        queryset = Item.objects.all()
        resource_name = 'items'
        include_resource_uri = False


class CustomerOrderResource(ModelResource):
    """Resource for Order model. Helps in creating new Orders for Customers."""
    user = fields.ForeignKey(UserResource, 'user', full=True)
    merchant = fields.ForeignKey(ProfileResource, 'merchant', full=True)
    store = fields.ForeignKey(StoreResource, 'store', full=True)
    items = fields.ManyToManyField(ItemResource, 'items', full=True)

    class Meta:
        queryset = Order.objects.all()
        resource_name = 'place_order'
        authentication = BasicAuthentication()
        authorization = ConsumerOrderResourceAuthorization()
        include_resource_uri = False

    def get_object_list(self, request):
        """Overrides the get_object_list method of ModelResource"""
        return super(CustomerOrderResource, self).get_object_list(request).filter(user=request.user)


class MerchantOrderResource(ModelResource):
    """Resource for Order model. Helps in viewing Orders from Customers to merchants."""
    items = fields.ToManyField(ItemResource, 'items', full=True)
    class Meta:
        queryset = Order.objects.all()
        resource_name = 'see_order'
        authentication = BasicAuthentication()
        authorization = MerchantOrderResourceAuthorization()
        include_resource_uri = False

    def get_object_list(self, request):
        """Overrides the get_object_list method of ModelResource"""
        print(request.user)
        print(Profile.objects.get(user=request.user).role)
        return super(MerchantOrderResource, self).get_object_list(request).filter(merchant__user=request.user)
