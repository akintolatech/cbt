from django import forms
from django.contrib.auth import get_user_model
from .models import Profile, ClassArm


class LoginForm(forms.Form):
    username = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter your SVC No (00/0000 format)',
                'maxlength': '7',
                'pattern': r'\d{2}/\d{4}'
            }
        )
    )


class UserRegistrationForm(forms.ModelForm):
    class_arm = forms.ModelChoiceField(
        queryset=ClassArm.objects.all(),
        required=True,
        label="Select your class"
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
            'password': forms.PasswordInput(
                attrs={
                    'placeholder': 'Enter your SVC No (00/0000 format)',
                    'maxlength': '7',
                    'pattern': r'\d{2}/\d{4}'
                }
            ),
        }
        labels = {
            'username': '',
            'password': '',
        }

        # Remove help text for all fields by setting an empty dictionary
        help_texts = {
            'username': None,
            'password': None,
        }


class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "password", 'email']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'phone_number']

        # Overriding the widget for the 'photo' field to include an id

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs.update({'id': 'image_input_id'})
