
from django import forms

from tester.models import Test


class CreateTestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description', 'image', 'is_active', 'form', 'mark', 'duration']