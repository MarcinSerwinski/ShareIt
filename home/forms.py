from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.core.exceptions import ValidationError

class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={
                                                                               'placeholder': 'Imię'}), label='')
    last_name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={
                                                                              'placeholder': 'Nazwisko'}), label='')
    email = forms.EmailField(max_length=128, widget=forms.EmailInput(attrs={
                                                                            'placeholder': 'Email'}), label='')
    password1 = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}), label='')

    password2 = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}), label='')

    class Meta:
        model = get_user_model()
        fields = ['email']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError('Hasła nie są takie same')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))


        if commit:
            user.save()

        return user

class UserEditAccessForm(forms.ModelForm):
    password = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}), label='')

    class Meta:
        model = get_user_model()
        fields = ['password']