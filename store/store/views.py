from django.contrib.auth.decorators import user_passes_test
from django.core.management import call_command
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def is_staff(user) -> bool:
    return bool(user.is_staff)


@user_passes_test(is_staff, login_url="/admin/login/")
def commands(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        call_command("reset")
        context = {"message": "Products have been reset successfully"}
    else:
        context = {}
    return render(request, "commands.html", context)
