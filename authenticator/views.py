from django.shortcuts import render


# Create your views here.
def index(request):
    msg = "Wired"

    context = {
        "msg": msg
    }

    return render(request, "authenticator/index.html", context)
