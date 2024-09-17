from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from .forms import (
    LoginForm,
    UserRegistrationForm,
    UserEditForm,
    ProfileEditForm
)
from .models import Profile


# Create your views here.
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
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
                    return render(request, "authenticator/dashboard.html", context)
                else:
                    return HttpResponse("You have been Banned from the system")
            else:
                form = LoginForm()
                return render(request, "authenticator/login.html", {"form": form, "error": "Invalid Login"})
    else:
        form = LoginForm()
    return render(request, "authenticator/login.html", {"form": form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            context = {
                'new_user': new_user,
                "success": "You have been successfully registered! Login to continue."
            }
            return render(
                request,
                'authenticator/registration-success.html',
                context
            )
    else:
        user_form = UserRegistrationForm()
    return render(
        request,
        'authenticator/register.html',
        {'user_form': user_form}
    )


@login_required
def edit_account(request):
    if request.method == "POST":
        user_form = UserEditForm(
            instance=request.user,
            data=request.POST
        )
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(
        request,
        'authenticator/edit-student.html',
        {
            'user_form': user_form,
            'profile_form': profile_form
        }
    )
