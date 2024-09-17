from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from .forms import LoginForm


# Create your views here.
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.post)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd["username"],
                password=cd["password"]
            )
            if user is not None:
                if user.is_active:
                    context = {
                        "msg": "wired"
                    }
                    login(request, user)
                    return render(request, "authenticator/student-dashboard.html", context)
                else:
                    return HttpResponse("Your Account is Inactive")
            else:
                return HttpResponse("Invalid Login")
        else:
            form = LoginForm()
        return render(request, "authenticator/login.html")


def register(request):
    msg = "Wired"

    context = {
        "msg": msg
    }

    return render(request, "authenticator/register.html", context)
