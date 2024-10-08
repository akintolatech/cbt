from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import (
    LoginForm,
    UserRegistrationForm,
    UserEditForm,
    ProfileEditForm
)
from .models import Profile
from tester.models import Test, TestResult


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
                    return redirect("authenticator:student_dashboard")
                else:
                    return HttpResponse("You have been Banned from the system")
            else:
                form = LoginForm()
            return render(request, "authenticator/login.html", {"form": form})
    else:
        form = LoginForm()
    return render(request, "authenticator/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect('authenticator:login')


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

            class_arm = user_form.cleaned_data.get('class_arm')
            # Create the user profile
            Profile.objects.create(user=new_user, class_arm=class_arm)
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
def student_dashboard(request):
    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user.profile)
    student_form = request.user.profile.class_arm.class_form
    tests = Test.objects.all().filter(form=student_form)
    results = TestResult.objects.all().filter(user_key=request.user)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        "tests": tests,
        "results": results
    }

    return render(request, "authenticator/student_dashboard.html", context)


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
