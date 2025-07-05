from datetime import timedelta

from django.contrib import messages
from django.shortcuts import render, redirect
from random import shuffle
from django.db.models import Avg, Sum, Count
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Test, TestResult, Question, TestSession
from django.utils.timezone import now




def test_questions(request, test_id):
    if not request.user.is_authenticated:
        return redirect('authenticator:login')

    test = get_object_or_404(Test, id=test_id)
    questions = list(test.question_set.all())[:60]
    shuffle(questions)

    available_results = TestResult.objects.filter(user_key=request.user.id)

    # if test in available_results:
    #     messages.error(request, "Insufficient funds for withdrawal.")
    #     return redirect("authenticator:student_dashboard")

    # Check if the user has already started the test
    session, created = TestSession.objects.get_or_create(user=request.user, test=test)

    if created:
        session.start_time = now()
        session.save()

    # Calculate remaining time
    end_time = session.start_time + timedelta(minutes=test.duration)
    remaining_time = (end_time - now()).total_seconds()

    if remaining_time <= 0:
        return redirect('tester:test_results')  # Redirect if time has expired

    context = {
        'test': test,
        'questions': questions,
        'remaining_time': int(remaining_time),
        'name': request.user.username,
    }

    return render(request, 'tester/test.html', context)



def mark_test(request, test_id):

    if not request.user.is_authenticated:
        return redirect('authenticator:register')

    test = get_object_or_404(Test, pk=test_id)
    session = get_object_or_404(TestSession, user=request.user, test=test)

    if session.is_completed:
        return redirect('tester:test_results')  # Prevent resubmission

    questions = Question.objects.filter(test=test)
    score = 0

    for question in questions:
        selected_option = request.POST.get(str(question.id))
        if selected_option == question.correct_option:
            score += test.mark

    TestResult.objects.create(
        user_key=request.user,
        class_arm_key=request.user.profile.class_arm,
        test_key=test,
        username=request.user.username,
        svc_no=request.user.password,
        class_arm=request.user.profile.class_arm.name,
        test=test.title,
        score=score,
        desc=test.description,
        date=now(),
    )

    session.is_completed = True
    session.save()

    return redirect('tester:test_results')



def test_results(request):
    results = TestResult.objects.filter(user_key=request.user)
    context = {

        'results': results,

    }
    return render(request, 'tester/results.html', context)
