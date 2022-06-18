#!/usr/bin/env python3

__author__ = "Surya Banerjee"

from rest_framework import serializers, status
from rest_framework.exceptions import APIException
from drf_writable_nested.serializers import WritableNestedModelSerializer

from autocompany.api.models import Product, Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']


class CartSerializer(WritableNestedModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['pk', 'cart_creation_time', 'delivery_time', 'order_completed', 'items']

    def validate_items(self, data):
        for item in data:
            if item['product'].stock < item['quantity']:
                e = APIException({"quantity": "higher number of quantity requested than in stock"})
                e.status_code = status.HTTP_400_BAD_REQUEST
                raise e
        return data

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data['user'] = request.user
        return super(CartSerializer, self).create(validated_data)


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['pk', 'name', 'overview']


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['pk', 'name', 'overview', 'model', 'year', 'stock', 'price']
