from django.db import models
from member.models import Member


# Defining database schema

class Shop(models.Model):
    title = models.CharField(max_length = 255)
    description = models.TextField()

    owner = models.OneToOneField(Member, on_delete = models.CASCADE)

    def __str__(self) -> str:
        return self.title

class Product(models.Model):
    title = models.CharField(max_length = 255)
    description = models.TextField()
    price = models.DecimalField(max_digits = 8, decimal_places = 2)
    image = models.ImageField(upload_to='images/')

    shop = models.ForeignKey(Shop, on_delete = models.CASCADE)

    def __str__(self) -> str:
        return self.title

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)      # Automatically sets current time when created
    modified_at = models.DateTimeField(auto_now = True)     # Automatically sets current time when updated/modified

    member = models.OneToOneField(Member, on_delete = models.CASCADE)

    # @property
    # def total_price(self):
    #     pass

    def __str__(self) -> str:
        return 'Cart of: ' + self.member.username

class Cart_item(models.Model):
    quantity = models.IntegerField(max_length = 3)

    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)

    def __str__(self) -> str:
        return f'Item: {self.product.title} for {self.cart.member.username}'

class Order(models.Model):
    PENDING = 'PD'
    PROCESSING = 'PR'
    DELIVERED = 'DL'
    CANCELLED = 'CL'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled'),
    ]

    order_status = models.CharField(max_length = 2, choices = STATUS_CHOICES, default = PENDING)
    created_at = models.DateTimeField(auto_now_add = True)

    member = models.ForeignKey(Member, null = True, on_delete = models.SET_NULL)
    shop = models.ForeignKey(Shop, null = True, on_delete = models.SET_NULL)

    # @property
    # def total_price(self):
    #     pass

    def __str__(self) -> str:
        if self.shop != None:
            return f'By: {self.member.username} from: {self.shop.title} ID: {self.pk}'
        else:
            return f'By: {self.member.username} from: REMOVED'

class Order_item(models.Model):
    quantity = models.IntegerField(max_length = 3)

    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, null = True, on_delete = models.SET_NULL)

    def __str__(self) -> str:
        if self.product != None:
            return f'Item: {self.product.title} for {self.order.member.username}'
        else:
            return f'Item: REMOVED for {self.order.member.username}'