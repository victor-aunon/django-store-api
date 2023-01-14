from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from .models import Product
from .serializers import ProductSerializer


class GetToken(ObtainAuthToken):
    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data.get("username"),
            password=serializer.validated_data.get("password"),
        )

        if not user:
            return Response(
                {"error": "Credentials are incorrect or user does not exist"},
                status=HTTP_404_NOT_FOUND,
            )
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "username": user.get_username(),
            },
            status=HTTP_200_OK,
        )


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-title")
    serializer_class = ProductSerializer
    pagination_class = LimitOffsetPagination
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
