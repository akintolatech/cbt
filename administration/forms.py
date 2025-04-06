
from django import forms

from tester.models import Test, Question

class QuestionUploadForm(forms.Form):
    file = forms.FileField(label='Upload .docx File')

class EditQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'form', 'subject', 'question_text', 'img', 'imginstr',
            'A', 'B', 'C', 'D', 'correct_option', 'test'
        ]

    def __init__(self, *args, **kwargs):
        super(EditQuestionForm, self).__init__(*args, **kwargs)
        # Optional: Customize field widgets or labels
        self.fields['question_text'].widget.attrs.update({'placeholder': 'Enter the question text'})
        self.fields['correct_option'].widget.attrs.update({'placeholder': 'e.g., A, B, C, or D'})





class CreateTestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description', 'image', 'is_active', 'form', 'mark', 'duration']