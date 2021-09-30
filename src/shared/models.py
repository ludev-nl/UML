from django.db import models


class Order(models.Model):
    deliverycompany = models.ForeignKey('DeliveryCompany', on_delete=models.CASCADE, null=True, related_name='ship')
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True, related_name='place')
    entry_date = models.CharField(max_length=255, default='')
    description = models.CharField(max_length=255, default='')
    order_number = models.CharField(max_length=255, default='')
    delivery_status = models.CharField(max_length=255, default='')
    pass


class Customer(models.Model):
    address = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    birth_date = models.CharField(max_length=255, default='')
    first_name = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    pass


class LineItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True, related_name='specifies')
    order = models.ForeignKey('Order', on_delete=models.CASCADE, null=True, related_name='consists')
    quantity = models.CharField(max_length=255, default='')
    pass


class Product(models.Model):
    product_number = models.CharField(max_length=255, default='')
    price = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    location = models.CharField(max_length=255, default='')
    description = models.CharField(max_length=255, default='')
    pass


class FlammableProduct(Product):
    pass


class RestrictedProduct(Product):
    pass


class DeliveryCompany(models.Model):
    name = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=255, default='')
    pass
