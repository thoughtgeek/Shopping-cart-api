
# **Shopping Cart Django**


## **User Stories:**

* As a company, I want all my products in a database, so I can offer them via our new platform to customers
* As a client, I want to add a product to my shopping cart, so I can order it at a later stage
* As a client, I want to remove a product from my shopping cart, so I can tailor the order to what I actually need
* As a client, I want to order the current contents in my shopping cart, so I can receive the products I need to repair my car
* As a client, I want to select a delivery date and time, so I will be there to receive the order
* As a client, I want to see an overview of all the products, so I can choose which product I want
* As a client, I want to view the details of a product, so I can see if the product satisfies my needs

# Setting up:

### Set up project and enter django shell:
```
$ sudo docker-compose up --build
$ sudo docker-compose exec web ./manage.py migrate
$ sudo docker-compose exec web ./manage.py shell
```


### Seed data, create new user and token

```
>>> from autocompany.api.seed_data import seed_products, get_seed_user_token
>>> seed_products()
>>> user, token = get_seed_user_token()
>>> user
<User: tyler>
>>> token
'9c15a107b4864cd58aac0c12acffc7df1b8b4874'
```


# Available APIs:
_(NOTE: Examples use this tool - https://httpie.io/)_</span>

## **Product API**

This is an unauthenticated API that can be used by the frontend to retrieve all product overviews and product details without requiring user log in.


### Retrieve the overview of all products
HTTP Method: GET \
API url: /api/product/

Example:
```
$ http localhost:8000/api/product/
HTTP/1.1 200 OK
Allow: GET
Content-Length: 607
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Referrer-Policy: same-origin
Vary: Accept
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

[
	{
    	"name": "MRF tyres",
    	"overview": "Pretty good tyres",
    	"pk": 1
	},
]
```


### Retrieve details of a product

HTTP Method: GET \
API url: /api/product/&lt;pk>/

Example:
```
$ http localhost:8000/api/product/1/
HTTP/1.1 200 OK
Allow: GET
Content-Length: 123
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Referrer-Policy: same-origin
Vary: Accept
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
	"model": "Honda City",
	"name": "MRF tyres",
	"overview": "Pretty good tyres",
	"pk": 1,
	"price": 1000,
	"stock": 10,
	"year": "2020-01-01"
}

```


## **Cart API**

This is an authenticated API(Token auth) to create, list and modify carts.

### Create a cart and add product to it without ordering them

HTTP Method: POST \
API url: /api/cart/ \
Header: 'Authorization: Token &lt;UserTokenGenerated>’

Example:
```
$ echo '{"items":[{"product":1,"quantity":2}]}' | http POST localhost:8000/api/cart/ 'Authorization: Token 9c15a107b4864cd58aac0c12acffc7df1b8b4874'
HTTP/1.1 201 Created
Allow: GET, POST
Content-Length: 159
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Referrer-Policy: same-origin
Vary: Accept
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
	"cart_creation_time": "2022-06-18T13:20:16.723071Z",
	"delivery_time": null,
	"items": [
    	{
        	"product": 1,
        	"quantity": 2
    	}
	],
	"order_completed": false,
	"pk": 1
}

```


### Remove a product from cart

HTTP Method: PATCH \
API url: /api/cart/&lt;pk>/ \
Header: 'Authorization: Token &lt;UserTokenGenerated>’

Example:
```
$ echo '{"items":[]}' | http PATCH localhost:8000/api/cart/1/ 'Authorization: Token 9c15a107b4864cd58aac0c12acffc7df1b8b4874'
HTTP/1.1 200 OK
Allow: GET, PATCH, DELETE
Content-Length: 133
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Referrer-Policy: same-origin
Vary: Accept
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
	"cart_creation_time": "2022-06-18T13:20:16.723071Z",
	"delivery_time": null,
	"items": [],
	"order_completed": false,
	"pk": 1
}
```


### Add a product to a cart

HTTP Method: PATCH \
API url: /api/cart/&lt;pk>/ \
Header: 'Authorization: Token &lt;UserTokenGenerated>’

Example:
```
echo '{"items":[{"product":1,"quantity":2}]}' | http PATCH localhost:8000/api/cart/1/ 'Authorization: Token 9c15a107b4864cd58aac0c12acffc7df1b8b4874'
HTTP/1.1 200 OK
Allow: GET, PATCH, DELETE
Content-Length: 159
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Referrer-Policy: same-origin
Vary: Accept
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
	"cart_creation_time": "2022-06-18T13:20:16.723071Z",
	"delivery_time": null,
	"items": [
    	{
        	"product": 1,
        	"quantity": 2
    	}
	],
	"order_completed": false,
	"pk": 1
}
```


### Order cart

HTTP Method: PATCH \
API url: /api/cart/&lt;pk>/ \
Header: 'Authorization: Token &lt;UserTokenGenerated>’

Example:
```
echo '{"order_completed":"true"}' | http PATCH localhost:8000/api/cart/1/ 'Authorization: Token 9c15a107b4864cd58aac0c12acffc7df1b8b4874'
HTTP/1.1 200 OK
Allow: GET, PATCH, DELETE
Content-Length: 158
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Referrer-Policy: same-origin
Vary: Accept
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
	"cart_creation_time": "2022-06-18T13:20:16.723071Z",
	"delivery_time": null,
	"items": [
    	{
        	"product": 1,
        	"quantity": 2
    	}
	],
	"order_completed": true,
	"pk": 1
}
```


### Set delivery date and time

HTTP Method: PATCH \
API url: /api/cart/&lt;pk>/ \
Header: 'Authorization: Token &lt;UserTokenGenerated>’

Example:
```
$ echo '{"delivery_time":"2022-06-18T13:20:16.723071Z"}' | http PATCH localhost:8000/api/cart/1/ 'Authorization: Token 9c15a107b4864cd58aac0c12acffc7df1b8b4874'
HTTP/1.1 200 OK
Allow: GET, PATCH, DELETE
Content-Length: 165
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Referrer-Policy: same-origin
Vary: Accept
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
	"cart_creation_time": "2022-06-18T13:20:16.723071Z",
	"delivery_time": "2022-06-18T13:20:16.723071Z",
	"items": [
    	{
        	"product": 1,
        	"quantity": 2
    	}
	],
	"order_completed": true,
	"pk": 1
}
```
