#!/usr/bin/env python3

__author__ = "Surya Banerjee"

import random
import string

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Product(models.Model):
    """
    This is the base model for storing the products that we sell.

    Here are some notes for each field -
    * Name: Name of the car part
    * Model: The car model the product is for
    * Year: Year of the car
    * Stock: Number of products available in inventory
    """

    name = models.CharField(max_length=255, unique=True)
    overview = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year = models.DateField()
    stock = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.pk}: {self.name}"


class Cart(models.Model):
    """
    This is the cart where we store the items ordered
    """

    delivery_time = models.DateTimeField(null=True, blank=True)
    order_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pk}: Completed - {self.order_completed}"


class CartItem(models.Model):
    """
    Each product ordered in a cart
    """

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, related_name="cartItems", null=True
    )
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"Item-{self.product.name} : Quantity-{self.quantity}"


@receiver(pre_save, sender=Cart)
def update_stock_on_cart_save(sender, instance, **kwargs):
    # If its a new cart and order is complete remove stock
    if instance.pk is None and instance.order_completed:
        update_stock(instance.items.all())

    # If existing cart is modified
    new_cart = instance
    old_cart = Cart.objects.get(pk=instance.pk)

    # If order is reversed, add stock back
    if old_cart.order_completed and not new_cart.order_completed:
        update_stock(new_cart.items.all(), add_stock=True)

    # If old cart order complete remove stock
    elif new_cart.order_completed and not old_cart.order_completed:
        update_stock(new_cart.items.all())


def update_stock(cartItems, add_stock=False):
        for item in cartItems:
            product = item.product

            if add_stock:
                product.stock = product.stock + item.quantity
            else:
                product.stock = product.stock - item.quantity

            product.save()
