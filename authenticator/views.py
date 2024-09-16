from django.shortcuts import render


# Create your views here.
def login_to_cbt(request):
    msg = "Wired"

    context = {
        "msg": msg
    }

    return render(request, "authenticator/login.html", context)

