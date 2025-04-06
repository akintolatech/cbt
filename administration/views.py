from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from authenticator.models import Profile, Form
from tester.models import (Test, Question, TestResult)
from django.db.models.functions import TruncDate
from django.db.models import Count, Sum
from datetime import date, timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from .forms import CreateTestForm

import json

@staff_member_required
def administration_dashboard(request):
    today = date.today()
    last_30_days = [today - timedelta(days=i) for i in range(30)]  # Fetch data for last 7 days

    context = {

        # from authenticator.models
        "total_classes": Form.objects.all().count(),
        "total_students": Profile.objects.all().count(),


        # from tester.models
        "total_tests": Test.objects.all().count(),
        "total_results": TestResult.objects.all().count(),
        "total_questions": Question.objects.all().count(),
    }

    return render(request, "administration/dashboard/administration_dashboard.html", context)


@staff_member_required
def test_mgmt(request):
    context = {

        "total_tests": Test.objects.all().count(),
        "tests": Test.objects.all(),
    }
    return render(request, "administration/test_mgmt/test_mgmt.html", context)


@staff_member_required
def create_test(request):
    if request.method == "POST":
        form = CreateTestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Test created successfully.")
            return redirect("administration:create_test")
    else:
        form = CreateTestForm()

    context = {
        "form": form,
    }
    return render(request, "administration/test_mgmt/create_test.html", context)


@staff_member_required
def edit_test(request, test_id):
    test = Test.objects.get(pk=test_id)
    # if request.method == "POST":
    #     form = CreateTestForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, "Test created successfully.")
    #         return redirect("administration:create_test")
    # else:
    #     form = CreateTestForm()
    #
    context = {
        "test": test,
    }
    return render(request, "administration/test_mgmt/create_test.html",context)