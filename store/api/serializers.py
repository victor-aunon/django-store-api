from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.exceptions import PermissionDenied, ValidationError

from .models import Product
from custom_types.product import ProductType


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "pk",
            "title",
            "price",
            "description",
            "category",
            "image",
            "amount",
            "rating",
            "rating_count",
        ]

    def create(self, validated_data: ProductType) -> Product:
        request: Request = self.context["request"]
        creator = request.user

        if not creator.is_staff:
            raise PermissionDenied("You are not allowed to edit products")

        return Product.objects.create(
            title=validated_data["title"],
            price=validated_data["price"],
            description=validated_data["description"],
            category=validated_data["category"],
            image=validated_data["image"],
            amount=validated_data["amount"],
        )

    def update(self, instance: Product, validated_data: ProductType) -> Product:

        if instance.amount + validated_data["amount"] < 0:
            raise ValidationError("Not so much stock available")

        instance.amount += validated_data["amount"]
        instance.save()

        return instance
