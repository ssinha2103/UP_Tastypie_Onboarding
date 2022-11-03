from django.contrib import admin
from django.urls import path

from django.conf.urls import url, include
from django.contrib import admin
from tastypie.api import Api
from api.resources import *


admin.autodiscover()
v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(ProfileResource())
v1_api.register(StoreResource())

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(v1_api.urls)),
]