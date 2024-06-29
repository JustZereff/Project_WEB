import os
import json
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


from .tasks import parse_and_save_news
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserEditForm, CustomPasswordChangeForm

def index(request):
    parse_and_save_news()
    
    # Определение пути для сохранения JSON файла
    script_dir = os.path.dirname(__file__)
    logs_dir = os.path.join(script_dir, 'logs')
    json_path = os.path.join(logs_dir, 'news_data.json')
        
    # Загрузка данных из JSON файла
    with open(json_path, 'r', encoding='utf-8') as json_file:
        news = json.load(json_file)

    return render(request, 'index/index.html', {'news': news})
        
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
    
@login_required
def user_settings(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        password_form = CustomPasswordChangeForm(request.user, request.POST)
        
        if 'update_profile' in request.POST:
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Ваш профіль успішно оновлено!')
                return redirect('user_settings')
        elif 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Ваш пароль успішно змінено!')
                return redirect('user_settings')
    else:
        user_form = UserEditForm(instance=request.user)
        password_form = CustomPasswordChangeForm(request.user)

    return render(request, 'user/user_settings.html', {
        'user_form': user_form,
        'password_form': password_form
    })

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'user/password_reset.html'
    email_template_name = 'user/password_reset_email.html'
    html_email_template_name = 'user/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'user/password_reset_subject.txt'
