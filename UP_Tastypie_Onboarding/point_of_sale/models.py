from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    MERCHANT = 1
    CONSUMER = 2

    ROLE_CHOICES = (
        (MERCHANT, 'MERCHANT'),
        (CONSUMER, 'CONSUMER')
    )

    name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=2)

    def __str__(self):
        return self.name

class Store(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    lat = models.FloatField()
    lng = models.FloatField()
    merchant = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="stores")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Stores'

class Item(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField()
    stores = models.ManyToManyField(Store)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Items"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    merchant = models.ForeignKey(Profile, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)

    class Meta:
        verbose_name_plural = "Orders"
