#!/usr/bin/env python3

__author__ = "Surya Banerjee"

from collections import OrderedDict

from django.urls import reverse
from django.test import TestCase, Client

from rest_framework import status
from rest_framework.test import APIClient

from autocompany.api.seed_data import seed_products, get_seed_user_token
from autocompany.api.models import Cart, CartItem, Product
from autocompany.api.serializers import (
    CartSerializer,
    CartItemSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
)


class ProductAPITest(TestCase):
    """
    Relevant User stories:

    1. As a company, I want all my products in a database, so I can offer them via our new platform to customers
    2. As a client, I want to see an overview of all the products, so I can choose which product I want
    3. As a client, I want to view the details of a product, so I can see if the product satisfies my needs
    """

    def setUp(self):
        seed_products()
        self.products = Product.objects.all()
        self.client = Client()

    def test_get_all_product_overview(self):
        response = self.client.get(reverse("product-list"))

        serializer = ProductListSerializer(self.products, many=True)

        # Should just contain minimal information about product
        self.assertEqual(
            [i for i in response.data[0].keys()], ["pk", "name", "overview"]
        )

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_product_detail(self):
        response = self.client.get(reverse("product-list") + "1/")

        product = self.products.get(pk=1)
        serializer = ProductDetailSerializer(product)

        # Should contain complete detailed information about product
        self.assertEqual(
            [i for i in response.data.keys()],
            ["pk", "name", "overview", "model", "year", "stock", "price"],
        )

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CartAPITest(TestCase):
    """
    Relevant User Stories:

    4. As a client, I want to add a product to my shopping cart, so I can order it at a later stage
    5. As a client, I want to order the current contents in my shopping cart, so I can receive the products I need to repair my car
    6. As a client, I want to remove a product from my shopping cart, so I can tailor the order to what I actually need
    7. As a client, I want to select a delivery date and time, so I will be there to receive the order
    """

    def setUp(self):
        seed_products()
        self.carts = Cart.objects.all()
        self.user, self.token = get_seed_user_token()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

    def test_create_list_cart(self):
        # Test creation of a new cart
        stock_before = Product.objects.get(pk=1).stock
        data = '{"items":[{"product":1,"quantity":2}],"delivery_time":"2022-10-1 00:00:00","order_completed":"true"}'
        response = self.client.post(
            reverse("cart-list"), data, content_type="application/json"
        )
        stock_after = Product.objects.get(pk=1).stock

        # Check stock has reduced after order
        self.assertLess(stock_after, stock_before)

        # Check stock has reduced exactly equal to order quantity
        self.assertEqual(stock_before - stock_after, 2)

        cart = Cart.objects.get(pk=response.data["pk"])
        serializer = CartSerializer(cart)

        self.assertEqual(
            OrderedDict(
                {
                    "product": cart.items.all()[0].product.pk,
                    "quantity": cart.items.all()[0].quantity,
                }
            ),
            response.data["items"][0],
        )
        self.assertEqual(serializer.data, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check existing carts
        response = self.client.get(reverse("cart-list"))
        all_carts = Cart.objects.all()
        serializer = CartSerializer(all_carts, many=True)

        self.assertEqual(serializer.data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_modify_cart(self):
        # Create cart which has not been ordered
        stock_before = Product.objects.get(pk=5).stock
        post_data = '{"items":[{"product":5,"quantity":10}],"order_completed":"false"}'
        response = self.client.post(
            reverse("cart-list"), post_data, content_type="application/json"
        )
        stock_after = Product.objects.get(pk=5).stock

        # Stock is not reduced since order not completed
        self.assertEqual(stock_before, stock_after)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Complete order
        stock_before = Product.objects.get(pk=5).stock
        patch_data = '{"order_completed": "true"}'
        response = self.client.patch(
            reverse("cart-list") + f"{response.data['pk']}/",
            patch_data,
            content_type="application/json",
        )
        stock_after = Product.objects.get(pk=5).stock

        # Check stock has reduced exactly equal to order quantity
        self.assertLess(stock_after, stock_before)
        self.assertEqual(stock_before - stock_after, 10)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Un-order cart
        stock_before = stock_after
        patch_data = '{"order_completed": "false"}'
        response = self.client.patch(
            reverse("cart-list") + f"{response.data['pk']}/",
            patch_data,
            content_type="application/json",
        )
        stock_after = Product.objects.get(pk=5).stock

        # Check stock has increased exactly equal to order quantity
        self.assertLess(stock_before, stock_after)
        self.assertEqual(stock_after - stock_before, 10)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Remove item from cart
        cart = Cart.objects.get(pk=response.data["pk"])
        self.assertGreater(cart.items.all().count(), 0)

        patch_data = '{"items": []}'
        response = self.client.patch(
            reverse("cart-list") + f"{response.data['pk']}/",
            patch_data,
            content_type="application/json",
        )
        self.assertEqual(cart.items.all().count(), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Set delivery date and time
        self.assertIsNone(cart.delivery_time)
        patch_data = '{"delivery_time":"2022-10-1 00:00:00"}'
        response = self.client.patch(
            reverse("cart-list") + f"{response.data['pk']}/",
            patch_data,
            content_type="application/json",
        )
        cart.refresh_from_db()
        self.assertIsNotNone(cart.delivery_time)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
