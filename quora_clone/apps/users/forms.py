from django.contrib.auth import get_user_model, forms
from django.core.exceptions import ValidationError

User = get_user_model()


class UserCreationForm(forms.UserCreationForm):
    error_message = forms.UserCreationForm.error_messages.update({
        'duplicate_username': 'This username has already been taken'
    })

    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = {'username', 'email', 'password1', 'password2', 'first_name', 'last_name', }

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
