#!/usr/bin/env python3

__author__ = "Surya Banerjee"

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from autocompany.api.models import Product, Cart, CartItem
from autocompany.api.serializers import (
    CartSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
)


class CartViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    serializer_class = CartSerializer
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class ProductViewset(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ProductListSerializer
    detail_serializer = ProductDetailSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        return Product.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            if hasattr(self, "detail_serializer"):
                return self.detail_serializer
        return super(ProductViewset, self).get_serializer_class()
