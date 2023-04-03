from django.contrib import admin
from . import models

# Registering models here so that they appear in the admin panel

admin.site.register(models.Shop)
admin.site.register(models.Product)
admin.site.register(models.Cart)
admin.site.register(models.Cart_item)
admin.site.register(models.Order)
admin.site.register(models.Order_item)
admin.site.register(models.Transaction)

