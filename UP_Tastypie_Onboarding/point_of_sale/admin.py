from django.contrib import admin

# Register your models here.
from .models import *

"""Registration of different models declared in models file"""
admin.site.register([Profile, Store, Item, Order])
