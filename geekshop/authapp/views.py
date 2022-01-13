from django.conf import settings
from django.contrib.auth.forms import UserChangeForm
from django.core.mail import send_mail
from django.forms import forms
from django.shortcuts import render
from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileForm
from django.contrib import auth
from django.urls import reverse

from authapp.models import ShopUser


def login(request):
    title = 'вход'

    login_form = ShopUserLoginForm(data=request.POST)
    next_url = request.GET.get('next', '')
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST:
                return HttpResponseRedirect(request.POST['next'])
            return HttpResponseRedirect(reverse('index'))

    content = {
        'title': title,
        'login_form': login_form,
        'next': next_url,
    }
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            send_verify_mail(user)
            return HttpResponseRedirect(reverse('authapp:login'))
    else:
        register_form = ShopUserRegisterForm()

    content = {
        'title': title,
        'register_form': register_form
    }

    return render(request, 'authapp/register.html', content)


def verify(request, email, activation_key):
    user = ShopUser.objects.filter(email=email).first()
    if user:
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.activation_key = None
            user.is_activation_key_expired = None
            user.save()
            auth.login(request, user)
    return render(request, 'authapp/verify.html')


def send_verify_mail(user):
    verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
    subject = 'Account verify'

    # title = f'Подтверждение учетной записи {user.username}'
    # message = f'{settings.BASE_URL}{verify_link}'

    message = f'Для подтверждения учетной записи {user.username} на портале \
{settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.BASE_URL}{verify_link}'

    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        edit_profile_form = ShopUserProfileForm(request.POST, instance=request.user.shopuserprofile)

        if edit_form.is_valid() and edit_profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('authapp:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        edit_profile_form = ShopUserProfileForm(request.POST, instance=request.user.shopuserprofile)

    context = {
        'title': title,
        'edit_form': edit_form,
        'edit_profile_form': edit_profile_form,
    }

    return render(request, 'authapp/edit.html', context)
