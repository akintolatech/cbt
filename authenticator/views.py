from django.shortcuts import render


# Create your views here.
def log_in(request):
    msg = "Wired"

    context = {
        "msg": msg
    }

    return render(request, "authenticator/login.html", context)


def register(request):
    msg = "Wired"

    context = {
        "msg": msg
    }

    return render(request, "authenticator/register.html", context)

