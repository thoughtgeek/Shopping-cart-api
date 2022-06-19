#!/usr/bin/env python3

__author__ = "Surya Banerjee"

from datetime import datetime
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from autocompany.api.models import Product

# We store the dummy products used in unit tests and seed data here
SEED_PRODUCTS = [
    {
        "name": "MRF tyres",
        "overview": "Pretty good tyres",
        "model": "Honda City",
        "year": datetime(2020, 1, 1),
        "stock": 10,
        "price": 1000,
        "id": 1,
    },
    {
        "name": "Goodyear tyres",
        "overview": "The best! just joking.",
        "model": "Toyota Lancer",
        "year": datetime(2009, 1, 1),
        "stock": 5,
        "price": 600,
        "id": 2,
    },
    {
        "name": "Wagner Brake Shoes",
        "overview": "Well, you know you brake a lot!",
        "model": "Honda Civic",
        "year": datetime(2014, 1, 1),
        "stock": 100,
        "price": 50,
        "id": 3,
    },
    {
        "name": "Bosch Windshield Wiper",
        "overview": "Lets you see while you run over someone in rain",
        "model": "Maruti Omni",
        "year": datetime(2001, 1, 1),
        "stock": 3,
        "price": 100,
        "id": 4,
    },
    {
        "name": "Michelin Tyres",
        "overview": "This one is the best, now I am serious!",
        "model": "Tesla Model X",
        "year": datetime(2021, 1, 1),
        "stock": 100,
        "price": 1500,
        "id": 5,
    },
    {
        "name": "Mobis Shock Absorber",
        "overview": "For all those adventures in the countryside",
        "model": "Hyundai Verna",
        "year": datetime(2017, 1, 1),
        "stock": 50,
        "price": 700,
        "id": 7,
    },
    {
        "name": "Lumax  Headlight",
        "overview": "Because our eyes can only see objects when light reflects on it",
        "model": "Volkswagen Polo GT",
        "year": datetime(2020, 1, 1),
        "stock": 200,
        "price": 900,
        "id": 8,
    },
]


def seed_products():
    for product in SEED_PRODUCTS:
        new_product = Product(**product)
        new_product.save()


def get_seed_user_token():
    user = User.objects.create_user("tyler", "tyler@awesometeam.nl", "awesomepassword")
    token = Token.objects.create(user=user)
    return user, token.key
