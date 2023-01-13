from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=120, help_text="The name of the product")
    price = models.FloatField(help_text="The price of the product")
    description = models.CharField(
        max_length=300, help_text="The description of the product"
    )
    category = models.CharField(
        max_length=100,
        choices=(
            ("uncategorized", "Uncategorized"),
            ("electronics", "Electronics"),
            ("jewelery", "Jewelry"),
            ("men's clothing", "Men's clothing"),
            ("women's clothing", "Women's clothing"),
        ),
        default="uncategorized",
        help_text="The category of the product",
    )
    image = models.URLField(help_text="The URL of the product image")
    amount = models.PositiveIntegerField(
        default=100, help_text="The number of products available in stock"
    )
    rating = models.FloatField(
        help_text="The product rating", default=0
    )
    rating_count = models.PositiveIntegerField(
        help_text="The number of ratings of the product", default=0
    )

    def __str__(self) -> str:
        return self.title
