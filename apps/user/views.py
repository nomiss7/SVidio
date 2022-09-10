from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from apps.user.forms import LoginForm, RegisterForm
from django.http import HttpResponseRedirect
from django.urls import reverse

from config.settings import PAGE_NAMES


def user_login(request):
    error = None
    next_page = request.GET.get('next', reverse('home'))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(username=cleaned_data['username'], password=cleaned_data['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(next_page)
                else:
                    error = 'Вы забанены, идите лесом -->'
            else:
                error = 'Неправильные логин или пароль'
    else:
        form = LoginForm()
    breadcrumbs = {'current': PAGE_NAMES['login']}
    return render(request, 'user/login.html', {'form': form, 'error': error,
                                               'breadcrumbs': breadcrumbs})


def user_logout(request):
    logout(request)
    return redirect('home')


def user_register(request):
    error = None
    next_page = request.GET.get('next', reverse('home'))
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            breadcrumbs = {'current': PAGE_NAMES['welcome']}
            return render(request, 'user/welcome.html', {'user': user, 'next_page': next_page,
                                                         'breadcrumbs': breadcrumbs})
        error = form.errors
    else:
        form = RegisterForm()
    breadcrumbs = {'current': PAGE_NAMES['register']}
    return render(request, 'user/register.html', {'form': form, 'error': error,
                                                  'breadcrumbs': breadcrumbs})
