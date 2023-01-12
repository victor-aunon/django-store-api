# Generated by Django 4.1.5 on 2023-01-12 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ProductRating",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("rate", models.FloatField(help_text="The product rating")),
                (
                    "count",
                    models.IntegerField(
                        help_text="The number of ratings of the product"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="The name of the product", max_length=120
                    ),
                ),
                ("price", models.FloatField(help_text="The price of the product")),
                (
                    "description",
                    models.CharField(
                        help_text="The description of the product", max_length=300
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("uncategorized", "Uncategorized"),
                            ("electronics", "Electronics"),
                            ("jewelery", "Jewelry"),
                            ("men's clothing", "Men's clothing"),
                            ("women's clothing", "Women's clothing"),
                        ],
                        default="uncategorized",
                        help_text="The category of the product",
                        max_length=100,
                    ),
                ),
                ("image", models.URLField(help_text="The URL of the product image")),
                (
                    "rating",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="api.productrating",
                    ),
                ),
            ],
        ),
    ]