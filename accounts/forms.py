from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username',
                               widget=forms.TextInput(attrs={
                                        'autocomplete': "off",
                                        'id': "username-input",
                                        'class': "input100",
                                        'type': "text",
                                        'name': "username",
                                        'placeholder': "Username",
                                                            }
                                                      )
                               )

    password = forms.CharField(label='Password',
                               widget=forms.TextInput(attrs={
                                    'class': "input100",
                                    'type': "password",
                                    'name': "pass",
                                    'placeholder': "Password",
                                    'id': 'password-input'
                                    })
                               )

    remember_me = forms.BooleanField(label="Remember Me",
                                     widget=forms.CheckboxInput(attrs={
                                        "id": "remember_me",
                                        }),
                                    required=False)

    # Validation checks
    def clean(self, *args, **kwargs):

        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)

        if not user:
            raise forms.ValidationError('Username password combination does not exist')

        if not user.is_active:
            raise forms.ValidationError('This account is suspended')

        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label='Username',
                              widget=forms.TextInput(attrs={
                                'autocomplete': "off",
                                'id': "username-input",
                                'class': "input100",
                                'type': "text",
                                'name': "username",
                                'placeholder': "Username",
                                })
                               )

    email = forms.EmailField(label='Email',
                             widget=forms.TextInput(attrs={
                                 'autocomplete': "off",
                                 'id': "email-input",
                                 'class': "input100",
                                 'type': "text",
                                 'name': "username",
                                 'placeholder': "Email",
                                 })
                            )

    password = forms.CharField(label='Password',
                               widget=forms.TextInput(attrs={
                                   'class': "input100",
                                   'type': "password",
                                   'name': "pass",
                                   'placeholder': "Password",
                                   'id': 'password-input'
                                    })
                                )

    password_confirm = forms.CharField(label='Confirm Password',
                                       widget=forms.TextInput(attrs={
                                           'class': "input100",
                                           'type': "password",
                                           'name': "pass_confirm",
                                           'placeholder': "Confirm Password",
                                           'id': 'password_confirm-input'
                                            })
                                        )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        user_query = User.objects.filter(username=username)
        email_query = User.objects.filter(email=email)

        if user_query.exists():
            raise forms.ValidationError(f"The username '{username}' is already taken")

        if email_query.exists():
            raise forms.ValidationError(f'An account is already associated with "{email}"')

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match")

        if len(password) < 10:
            raise forms.ValidationError("Passwords must be at least 10 characters long")

        return super(UserRegisterForm, self).clean(*args, **kwargs)
