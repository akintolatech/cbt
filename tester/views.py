from django.shortcuts import render, redirect
from random import shuffle
from django.db.models import Avg, Sum, Count
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Test, TestResult, Question
from django.utils import timezone

now = timezone.now()


# Create your views here.
def test_questions(request, test_id):
    if request.user.is_authenticated:
        tests = Test.objects.get(id=test_id)
        questions = list(tests.question_set.all())
        shuffle(questions)  # Shuffle the list of questions

        context = {
            'test': tests,
            'questions': questions,  # Pass the shuffled list of questions to the template
            'name': request.user.username,
        }

        return render(request, 'tester/test.html', context)

    else:
        return redirect('login')


@csrf_exempt
def mark_test(request, test_id):
    if request.user.is_authenticated:

        test = get_object_or_404(Test, pk=test_id)
        questions = Question.objects.all()

        # all_results = results.objects.filter(user=request.user)
        score = 0

        for question in questions:

            if request.POST.get(str(question.id)) == question.correct_option:
                score += test.mark

        TestResult.objects.create(
            user_key=request.user,
            class_arm_key=request.user.profile.class_arm,
            test_key=test,

            username=request.user.username,
            svc_no=request.user.password,
            class_arm=request.user.profile.class_arm.name,
            test=test,
            score=score,

            desc=test.description,
            date=now,
        )

        # Calculate the total score by summing all TestResult scores for the user
        # total_score = TestResult.objects.filter(user=request.user).aggregate(Sum('score'))['score__sum']

        # Increment the user's total_score
        # request.user.total_score = total_score
        # request.user.save()
        # context = {
        #     "total": test.ace,
        #     "results": all_results,
        # }

        return redirect('tester:test_results')
        # return render(request, 'authenticator/results.html', context)
    else:
        return redirect('authenticator:register')


def test_results(request):
    results = TestResult.objects.filter(user_key=request.user)
    context = {

        'results': results,

    }
    return render(request, 'tester/results.html', context)
