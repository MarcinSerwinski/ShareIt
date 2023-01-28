from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Imię'}), label='')
    last_name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}), label='')
    email = forms.EmailField(max_length=128, widget=forms.EmailInput(attrs={'placeholder': 'Email'}), label='')
    password1 = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}), label='')
    password2 = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}),
                                label='')

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class UserEditAccessForm(forms.ModelForm):
    password = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}), label='')

    class Meta:
        model = get_user_model()
        fields = ['password']


class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Imię'}), label='')
    last_name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}), label='')
    email = forms.EmailField(max_length=128, widget=forms.EmailInput(attrs={'placeholder': 'Email'}), label='')

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name']


class UserEditPasswordForm(forms.ModelForm):
    old_password = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Stare hasło'}),
                                   label='')
    password1 = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Nowe hasło'}),
                                label='')
    password2 = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz nowe hasło'}),
                                label='')

    class Meta:
        model = get_user_model()
        fields = []


class NewPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']
