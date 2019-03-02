from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import forms as auth_forms
from django.core.exceptions import ValidationError

User = get_user_model()


class UserCreationForm(auth_forms.UserCreationForm):
    error_message = auth_forms.UserCreationForm.error_messages.update({
        'duplicate_username': 'This username has already been taken'
    })

    class Meta(auth_forms.UserCreationForm.Meta):
        model = User
        fields = {'username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'gender'}

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'johndoe23'
        self.fields['email'].widget.attrs['placeholder'] = 'johndoe@email.com'
        self.fields['password1'].widget.attrs['placeholder'] = '*********'
        self.fields['password2'].widget.attrs['placeholder'] = '*********'
        self.fields['first_name'].widget.attrs['placeholder'] = 'John'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Doe'

    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages['duplicate_username'])


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile_image', 'gender', 'description']
        widgets = {
            'description': forms.Textarea(attrs={
                'cols': 40,
                'rows': 5,
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['gender'].widget.attrs['class'] = 'ui fluid dropdown'
