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
from .forms import CreateTestForm, EditQuestionForm, QuestionUploadForm
import re
import json


from docx import Document

@staff_member_required
def upload_questions(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    form = QuestionUploadForm()
    success = 0
    failed = []

    if request.method == 'POST':
        form = QuestionUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            content = file.read().decode('utf-8')

            # Split the text into blocks (questions separated by blank lines)
            blocks = re.split(r'\n\s*\n', content.strip())

            for block in blocks:
                lines = block.strip().splitlines()
                question_data = {
                    'question': '',
                    'options': {},
                    'correct_key': '',
                }

                for line in lines:
                    line = line.strip()

                    # Detect options like A. Text
                    match = re.match(r'^([A-Da-d])\.\s*(.+)$', line)
                    if match:
                        key, val = match.groups()
                        question_data['options'][key.upper()] = val.strip()

                    # Detect answer like ANSWER: C
                    elif line.lower().startswith('answer:'):
                        match = re.match(r'^answer\s*[:\-–]?\s*([A-Da-d])$', line, re.IGNORECASE)
                        if match:
                            question_data['correct_key'] = match.group(1).strip().upper()

                    # Assume the first non-option, non-answer line is the question
                    elif not question_data['question']:
                        question_data['question'] = line

                # Validate and store
                if (question_data['question']
                        and question_data['correct_key'] in question_data['options']
                        and len(question_data['options']) == 4):

                    try:
                        correct_option_text = question_data['options'][question_data['correct_key']]

                        Question.objects.create(
                            question_text=question_data['question'],
                            test=test,
                            A=question_data['options'].get('A', ''),
                            B=question_data['options'].get('B', ''),
                            C=question_data['options'].get('C', ''),
                            D=question_data['options'].get('D', ''),
                            correct_option=correct_option_text  # ✅ Save the full text here
                        )
                        success += 1

                    except Exception as e:
                        failed.append({'question': question_data['question'], 'error': str(e)})

                else:
                    failed.append({'question': question_data.get('question', 'Unknown'), 'error': 'Bad formatting or missing data'})

            return render(request, "administration/test_mgmt/upload_questions.html", {
                'form': form,
                'success_count': success,
                'failed': failed,
                'test': test
            })

    return render(request, "administration/test_mgmt/upload_questions.html", {
        'form': form,
        'test': test
    })

# def upload_questions(request, test_id):
#     test = get_object_or_404(Test, id=test_id)
#     form = QuestionUploadForm()
#     success = 0
#     failed = []
#
#     if request.method == 'POST':
#         form = QuestionUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             file = request.FILES['file']
#             content = file.read().decode('utf-8')
#
#             # Split into blocks of questions
#             blocks = re.split(r'\n\s*\n', content.strip())
#             for block in blocks:
#                 lines = block.strip().splitlines()
#                 question_data = {
#                     'question': '',
#                     'options': {},
#                     'correct_option': ''
#                 }
#
#                 for line in lines:
#                     line = line.strip()
#
#                     # Check for options
#                     match = re.match(r'^([A-Da-d])\.\s*(.+)$', line)
#                     if match:
#                         key, val = match.groups()
#                         question_data['options'][key.upper()] = val.strip()
#
#                     # Check for answer line
#                     elif line.lower().startswith("answer:"):
#                         match = re.match(r'^answer\s*[:\-–]?\s*(.+)$', line, re.IGNORECASE)
#                         if match:
#                             question_data['correct_option'] = match.group(1).strip()
#
#                     # Else assume it's the question
#                     elif not question_data['question']:
#                         question_data['question'] = line
#
#                 if (question_data['question'] and question_data['correct_option']
#                     and len(question_data['options']) == 4):
#                     try:
#                         Question.objects.create(
#                             question_text=question_data['question'],
#                             test=test,
#                             A=question_data['options'].get('A', ''),
#                             B=question_data['options'].get('B', ''),
#                             C=question_data['options'].get('C', ''),
#                             D=question_data['options'].get('D', ''),
#                             correct_option=question_data['correct_option']
#                         )
#                         success += 1
#                     except Exception as e:
#                         failed.append({'question': question_data['question'], 'error': str(e)})
#                 else:
#                     failed.append({'question': question_data['question'], 'error': 'Missing fields or badly formatted'})
#
#             return render(request, "administration/test_mgmt/upload_questions.html", {
#                 'form': form,
#                 'success_count': success,
#                 'failed': failed,
#                 'test': test
#             })
#
#     return render(request, "administration/test_mgmt/upload_questions.html", {
#         'form': form,
#         'test': test
#     })

# def upload_questions(request, test_id):
#     test = get_object_or_404(Test, id=test_id)
#     form = QuestionUploadForm()
#     success = 0
#     failed = []
#
#     if request.method == 'POST':
#         form = QuestionUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             file = request.FILES['file']
#             document = Document(file)
#
#             raw_text = "\n".join([p.text.strip() for p in document.paragraphs if p.text.strip()])
#             # Split questions by two or more line breaks or 'ANSWER:' keyword
#             question_blocks = re.split(r'(?:ANSWER[:\-–]?\s*[A-Da-d])', raw_text)
#             answers = re.findall(r'ANSWER[:\-–]?\s*([A-Da-d])', raw_text)
#
#             if len(answers) != len(question_blocks) - 1:
#                 failed.append({'question': 'Parsing error', 'error': 'Mismatch between questions and answers'})
#             else:
#                 for idx in range(len(answers)):
#                     block = question_blocks[idx].strip()
#                     answer = answers[idx].strip().upper()
#
#                     # Parse question and options
#                     lines = block.splitlines()
#                     question_text = ''
#                     options = {}
#
#                     for line in lines:
#                         line = line.strip()
#                         if not question_text and not re.match(r'^[A-Da-d]\.', line):
#                             question_text = line
#                         elif re.match(r'^[A-Da-d]\.', line):
#                             match = re.match(r'^([A-Da-d])\.\s*(.+)', line)
#                             if match:
#                                 key, val = match.groups()
#                                 options[key.upper()] = val.strip()
#
#                     if question_text and answer in options:
#                         try:
#                             Question.objects.create(
#                                 question_text=question_text,
#                                 test=test,
#                                 A=options.get('A', ''),
#                                 B=options.get('B', ''),
#                                 C=options.get('C', ''),
#                                 D=options.get('D', ''),
#                                 correct_option=answer
#                             )
#                             success += 1
#                         except Exception as e:
#                             failed.append({'question': question_text, 'error': str(e)})
#                     else:
#                         failed.append({'question': question_text or 'Unknown', 'error': 'Invalid format or missing option/answer'})
#
#             return render(request, "administration/test_mgmt/upload_questions.html", {
#                 'form': form,
#                 'success_count': success,
#                 'failed': failed,
#                 'test': test
#             })
#
#     return render(request, "administration/test_mgmt/upload_questions.html", {
#         'form': form,
#         'test': test
#     })

# def upload_questions(request, test_id):
#     test = get_object_or_404(Test, id=test_id)
#     form = QuestionUploadForm()
#     success = 0
#     failed = []
#
#     if request.method == 'POST':
#         form = QuestionUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             file = request.FILES['file']
#             document = Document(file)
#
#             questions = []
#
#             for para in document.paragraphs:
#                 text = para.text.strip()
#                 if not text:
#                     continue
#
#                 lines = [line.strip() for line in text.split('\n') if line.strip()]
#                 if len(lines) < 3:
#                     # Split manually in case everything is in one string
#                     lines = re.split(r'\r?\n', text)
#
#                 question_data = {
#                     'question': '',
#                     'options': {},
#                     'answer_text': ''
#                 }
#
#                 for line in lines:
#                     line = line.strip()
#
#                     if re.match(r'^[A-Da-d]\.', line):  # A. 0.5
#                         parts = line.split('.', 1)
#                         if len(parts) == 2:
#                             key = parts[0].strip().upper()
#                             val = parts[1].strip()
#                             if key in ['A', 'B', 'C', 'D']:
#                                 question_data['options'][key] = val
#
#                     elif line.lower().startswith('answer'):
#                         match = re.search(r'answer\s*[:\-–]?\s*(.+)', line, re.IGNORECASE)
#                         if match:
#                             question_data['answer_text'] = match.group(1).strip()
#
#                     elif not question_data['question']:
#                         question_data['question'] = line  # First line is the question
#
#                 if question_data['question'] and question_data['answer_text']:
#                     questions.append(question_data)
#
#             # Save questions to the database
#             for q in questions:
#                 try:
#                     Question.objects.create(
#                         question_text=q['question'],
#                         test=test,
#                         A=q['options'].get('A', ''),
#                         B=q['options'].get('B', ''),
#                         C=q['options'].get('C', ''),
#                         D=q['options'].get('D', ''),
#                         correct_option=q['answer_text']
#                     )
#                     success += 1
#                 except Exception as e:
#                     failed.append({'question': q.get('question'), 'error': str(e)})
#
#             return render(request, "administration/test_mgmt/upload_questions.html", {
#                 'form': form,
#                 'success_count': success,
#                 'failed': failed,
#                 'test': test
#             })
#
#     return render(request, "administration/test_mgmt/upload_questions.html", {
#         'form': form,
#         'test': test
#     })


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
    questions = Question.objects.filter(test=test_id)
    if request.method == "POST":
        form = EditQuestionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Test created successfully.")
            return redirect("administration:edit_test")
    else:
        form = EditQuestionForm()

    context = {
        "test": test,
        "questions": questions,
        "form": form
    }
    return render(request, "administration/test_mgmt/edit_test.html",context)