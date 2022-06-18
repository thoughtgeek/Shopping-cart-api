#!/usr/bin/env python3

__author__ = "Surya Banerjee"

import random
import string

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.contrib.auth.models import User


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

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    cart_creation_time = models.DateTimeField(null=True, blank=True, default=now)
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


@receiver(pre_save, sender=CartItem)
def update_stock_for_new_cart(sender, instance, **kwargs):
    # If its a new cart and order is complete remove stock
    if instance.pk is None and instance.cart.order_completed:
        update_stock(instance)

@receiver(pre_save, sender=Cart)
def update_stock_for_existing_carts(sender, instance, **kwargs):
    # If existing cart is modified
    if instance.pk is not None:
        new_cart = instance
        old_cart = Cart.objects.get(pk=instance.pk)

        # If order is reversed, add stock back
        if old_cart.order_completed and not new_cart.order_completed:
            for item in instance.items.all():
                update_stock(item, add_stock=True)

        # If old cart order complete remove stock
        elif new_cart.order_completed and not old_cart.order_completed:
            for item in instance.items.all():
                update_stock(item)

def update_stock(item, add_stock=False):
        product = item.product

        if add_stock:
            product.stock = product.stock + item.quantity
        else:
            product.stock = product.stock - item.quantity

        product.save()
