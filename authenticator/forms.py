from django import forms
from django.contrib.auth import get_user_model


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='Repeat password',
        widget=forms.PasswordInput
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data

        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']


# class NameForm(forms.ModelForm):
#     CHOICES = (
#
#         ('JSS1 A', 'JSS1 A'),
#         ('JSS1 B', 'JSS1 B'),
#         ('JSS1 C', 'JSS1 C'),
#         ('JSS1 D', 'JSS1 D'),
#         ('JSS1 E', 'JSS1 E'),
#
#         ('JSS2 A', 'JSS2 A'),
#         ('JSS2 B', 'JSS2 B'),
#         ('JSS2 C', 'JSS2 C'),
#         ('JSS2 D', 'JSS2 D'),
#         ('JSS2 E', 'JSS2 E'),
#
#         ('JSS3 A', 'JSS3 A'),
#         ('JSS3 B', 'JSS3 B'),
#         ('JSS3 C', 'JSS3 C'),
#         ('JSS3 D', 'JSS3 D'),
#         ('JSS3 E', 'JSS3 E'),
#         ('JSS3 F', 'JSS3 F'),
#
#         ('SSS1 ART', 'SSS1 ART'),
#         ('SSS1 COMMERCIAL', 'SSS1 COMMERCIAL'),
#         ('SSS1 SCIENCE A', 'SSS1 SCIENCE A'),
#         ('SSS1 SCIENCE B', 'SSS1 SCIENCE B'),
#         ('SSS1 TECHNICAL A', 'SSS1 TECHNICAL A'),
#         ('SSS1 TECHNICAL B', 'SSS1 TECHNICAL B'),
#
#         ('SSS2 ARTCOMM', 'SSS2 ARTCOMM'),
#         ('SSS2 SCIENCE A', 'SSS2 SCIENCE A'),
#         ('SSS2 SCIENCE B', 'SSS2 SCIENCE B'),
#         ('SSS2 TECHNICAL A', 'SSS2 TECHNICAL A'),
#         ('SSS2 TECHNICAL B', 'SSS2 TECHNICAL B'),
#
#         ('SSS3 ART', 'SSS3 ART'),
#         ('SSS3 COMMERCIAL', 'SSS3 COMMERCIAL'),
#         ('SSS3 SCIENCE', 'SSS3 SCIENCE'),
#         ('SSS3 TECHNICAL', 'SSS3 TECHNICAL'),
#         ('SSS3 SCIENCE AND TECHNICAL', 'SSS3 SCIENCE AND TECHNICAL'),
#
#     )
#
#     classes = forms.ChoiceField(choices=CHOICES, widget=forms.Select)
#
#     class Meta:
#         model = StudentUser
#         fields = ('username', 'password', 'classes')
