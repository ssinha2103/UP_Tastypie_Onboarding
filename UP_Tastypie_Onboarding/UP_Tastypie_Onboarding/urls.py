from django.contrib import admin
from django.urls import path

from django.conf.urls import url, include
from django.contrib import admin
from tastypie.api import Api
from api.resources import *


admin.autodiscover()
"""providing name to API. in output it reflects as :- http://127.0.0.1:8000/api/v1/users/ and etc.. """
v1_api = Api(api_name='v1')

"""Registration of different resources ."""
v1_api.register(UserResource())
v1_api.register(ProfileResource())
v1_api.register(StoreResource())
v1_api.register(ItemResource())

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(v1_api.urls)),
]
