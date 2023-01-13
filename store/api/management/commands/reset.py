from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from typing import List
import requests

from api.models import Product, ProductRating
from custom_types.product import ProductType


class Command(BaseCommand):
    help = "Reset Products table"

    BASE_API_URL = "https://fakestoreapi.com"

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        ProductRating.objects.all().delete()

        products: List[ProductType] = requests.get(
            f"{self.BASE_API_URL}/products"
        ).json()

        if not products:
            raise ObjectDoesNotExist("There are no products")

        for product in products:
            rating_db = ProductRating(**product["rating"])
            rating_db.save()
            product.pop("rating")
            product_db = Product(
                **product,
                rating=ProductRating.objects.get(pk=product["id"]),
            )
            product_db.save()
