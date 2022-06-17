#!/usr/bin/env python3

__author__ = "Surya Banerjee"

from django.urls import path
from django.contrib import admin
from django.conf.urls import include

from rest_framework.routers import DefaultRouter
from autocompany.api.views import CartViewset, ProductViewset


router = DefaultRouter()
router.register(r"cart", CartViewset, basename="cart")
router.register(r"product", ProductViewset, basename="product")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
]
