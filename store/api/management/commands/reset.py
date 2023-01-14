from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
import requests

from api.models import Product


class Command(BaseCommand):
    help = "Reset Products table"

    BASE_API_URL = "https://fakestoreapi.com"

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()

        products = requests.get(
            f"{self.BASE_API_URL}/products"
        ).json()

        if not products:
            raise ObjectDoesNotExist("There are no products")

        for product in products:
            rating = product["rating"]
            product.pop("rating")
            product_db = Product(
                **product, rating=rating["rate"], rating_count=rating["count"]
            )
            product_db.save()
