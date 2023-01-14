from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from .api_views import GetToken, ProductViewSet


class APITest(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.products_view = ProductViewSet.as_view({"get": "retrieve"})
        self.products_view_list = ProductViewSet.as_view({"get": "list"})
        self.products_view_create = ProductViewSet.as_view({"post": "create"})
        self.product_test_props = {
            "title": "Testproduct",
            "price": 15,
            "description": "This is a test product",
            "category": "uncategorized",
            "image": "http://products.com/testproduct",
            "amount": 50,
        }
        self.test_user = {"username": "testuser", "password": "testpassword1234"}

    def create_user(self) -> None:
        self.user = User.objects.create_user(
            username=self.test_user["username"],
            password=self.test_user["password"],
            is_staff=True,
        )

    def get_token(self) -> int:
        self.create_user()
        request = self.factory.post(
            "/api/token/",
            {
                "username": self.test_user["username"],
                "password": self.test_user["password"],
            },
        )
        response: Response = GetToken.as_view()(request)
        response.render()
        self.user_token = response.data["token"]
        return int(response.status_code)

    def create_product(self) -> int:
        self.get_token()
        request = self.factory.post("/api/products/", self.product_test_props)
        force_authenticate(request, user=self.user, token=self.user_token)
        response: Response = self.products_view_create(request)
        return int(response.status_code)

    def test_create_user(self) -> None:
        """Creating a user who is part of the staff"""
        self.create_user()
        user = User.objects.get(pk=1)
        self.assertEquals(user.username, self.test_user["username"])

    def test_get_auth_token(self) -> None:
        """Getting an authorization token for the created user"""
        status_code = self.get_token()
        self.assertEquals(status_code, 200)

    def test_creating_product_not_authenticated(self) -> None:
        """Posting a new product without authentication result in a 401 error"""
        request = self.factory.post("/api/products/", self.product_test_props)
        response: Response = self.products_view_list(request)
        self.assertEquals(response.status_code, 401)

    def test_creating_product_authenticated(self) -> None:
        """Successfully posting a new product with authentication"""
        status_code = self.create_product()
        self.assertEquals(status_code, 201)

    def test_listing_products(self) -> None:
        """Test that a product list is shown with non authenticated user"""
        self.create_product()
        request = self.factory.get("/api/products/")
        response: Response = self.products_view(request, pk=1)
        response.render()
        self.assertEquals(response.data["title"], self.product_test_props["title"])
