from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser

from .views import commands


class TestCommandsView(TestCase):
    """Test the commands view"""

    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = {"username": "testuser", "password": "test1234"}

    def test_commands_view_not_authenticated(self) -> None:
        request = self.factory.get("/commands")
        request.user = AnonymousUser()
        response = commands(request)
        # Unauthenticated user is redirected to /admin/login. Code 302
        self.assertEquals(response.status_code, 302)

    def test_commands_view_user_is_not_staff(self) -> None:
        request = self.factory.get("/commands")
        request.user = User.objects.create_user(
            username=self.user["username"], password=self.user["password"]
        )
        response = commands(request)
        # User who is not part of the staff is redirected to /admin/login. Code 302
        self.assertEquals(response.status_code, 302)

    def test_commands_view_user_is_staff(self) -> None:
        request = self.factory.get("/commands")
        request.user = User.objects.create_user(
            username=self.user["username"],
            password=self.user["password"],
            is_staff=True,
        )
        response = commands(request)
        self.assertEquals(response.status_code, 200)
        self.assertInHTML(
            '<input type="submit" value="Reset Products">',
            response.getvalue().decode("utf-8"),
        )
