from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'birth_date']
        labels = {
            'first_name': "Ім'я",
            'last_name': 'Прізвище',
            'email': 'Електронна пошта',
            'birth_date': 'Дата народження'
        }
        
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

class CustomAuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
        
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Старий пароль'
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Новий пароль'
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Підтвердіть новий пароль'
    )