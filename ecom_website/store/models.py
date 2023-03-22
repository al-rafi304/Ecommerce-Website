from django.db import models

# Defining database schema

class User(models.Model):
    name = models.CharField(max_length = 255)
    email = models.EmailField(unique = True)
    phone = models.CharField(max_length = 50)
    dob = models.DateField()
    is_seller = models.BooleanField(default = False)

    def __str__(self) -> str:
        return self.name

class Shop(models.Model):
    title = models.CharField(max_length = 255)
    description = models.TextField()

    owner = models.OneToOneField(User, on_delete = models.CASCADE)

    def __str__(self) -> str:
        return self.title

class Product(models.Model):
    title = models.CharField(max_length = 255)
    description = models.TextField()
    price = models.DecimalField(max_digits = 8, decimal_places = 2)

    shop = models.ForeignKey(Shop, on_delete = models.CASCADE)

    def __str__(self) -> str:
        return self.title

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)      # Automatically sets current time when created
    modified_at = models.DateTimeField(auto_now = True)     # Automatically sets current time when updated/modified

    user = models.ForeignKey(User, on_delete = models.CASCADE)

    # @property
    # def total_price(self):
    #     pass

    def __str__(self) -> str:
        return 'Cart of: ' + self.user.name

class Cart_item(models.Model):
    quantity = models.IntegerField(max_length = 3)

    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)

    def __str__(self) -> str:
        return f'Item: {self.product.title} for {self.cart.user.name}'

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

    user = models.ForeignKey(User, null = True, on_delete = models.SET_NULL)
    shop = models.ForeignKey(Shop, null = True, on_delete = models.SET_NULL)

    # @property
    # def total_price(self):
    #     pass

    def __str__(self) -> str:
        return f'By: {self.user.name} from: {self.shop.title}'

class Order_item(models.Model):
    quantity = models.IntegerField(max_length = 3)

    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, null = True, on_delete = models.SET_NULL)

    def __str__(self) -> str:
        return f'Item: {self.product.title} for {self.order.user.name}'