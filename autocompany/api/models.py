import random
import string

from django.db import models


def randomstr_generator():
    chars = string.ascii_lowercase + string.digits
    randomstr = "".join((random.choice(chars)) for x in range(10))
    return randomstr

class Product(models.Model):
    """
    This is the base model for storing the products that we sell.

    Here are some notes for each field -
    * Name: We assume that multiple parts might have same name, hence not set unique.
    * Product Id: This is the unique id to use for a product
    * Model: The car model the product is for
    * Year: Year of the car
    * Stock: Number of products available in inventory
    """

    name = models.CharField(max_length=255)
    product_id = models.CharField(
        max_length=255, unique=True, default=randomstr_generator
    )
    overview = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year = models.DateField()
    stock = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}: {self.product_id}"


class Cart(models.Model):
    """
    This is the cart where we store the items ordered
    """

    products = models.ManyToManyField(Product)
    delivery_time = models.DateTimeField(null=True, blank=True)
    order_completed = models.BooleanField(default=False)
