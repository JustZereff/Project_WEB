from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def index(request):
    return render(request, 'index/index.html')

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'registration/login.html', {'form': form, 'error': 'Невірний email або пароль!'})
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class CustomLogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('index'))

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'user/password_reset.html'
    email_template_name = 'user/password_reset_email.html'
    html_email_template_name = 'user/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'user/password_reset_subject.txt'
