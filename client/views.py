from django.urls import reverse
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.dispatch import receiver
from django.contrib import messages
from client.forms import *

# email confirmation
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from client.tokens import account_activation_token
from django.utils.encoding import force_text

# models
from client.models import User

# render home page
def index(request):
    return render(request, "index.html") 

# sign up with email confirmation
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Welcome to Thinkspace. Please activate your account.'
            message = render_to_string('email/account_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            messages.success(request, 'Your account has been created. Please check your email for a link to verify your account.')
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/sign_up.html', {'form': form})

# detect logins and logouts
@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    flash_this = user.first_name or user.username
    messages.success(request, 'Hello, {}. You are now logged in.'.format(flash_this))

@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    messages.success(request, 'You have been logged out.')

# activate account via email
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Your account has been verified.')
        return redirect('index')
    else:
        messages.error(request, 'Your account could not be verified.')
        return redirect('index')

# change password mechanism
@require_POST
def change_password(request):
    form = PasswordChangeForm(request.user, request.POST)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)  # Important!
        messages.success(
            request, 'Your password was successfully changed.')
    else:
        messages.error(request, 'Your password could not be changed. Please correct any errors.')
    return redirect('dashboard')

# render dashboard
def dashboard(request):
    if request.method == 'POST':
        if "photo" in request.POST:
            form = DashboardPhotoForm(request.POST, instance=request.user)
        if "about" in request.POST:
            form = DashboardAboutForm(request.POST, instance=request.user)
        if "basic_info" in request.POST:
            form = DashboardBasicInfoForm(request.POST, instance=request.user)
        if "resume" in request.POST:
            form = DashboardResumeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your information was successfully changed.')
        else:
            messages.error(
                request, 'Your information could not be changed. Please correct any errors.')
        return redirect('dashboard')
    else:
        password_change_form = PasswordChangeForm(request.user)
        basic_info_form = DashboardBasicInfoForm(instance=request.user)
        about_form = DashboardAboutForm(instance=request.user)
        photo_form = DashboardPhotoForm(instance=request.user)
        resume_form = DashboardResumeForm(instance=request.user)
    return render(request, 'dashboard.html', {
        'password_change_form' : password_change_form,
        'basic_info_form': basic_info_form,
        'about_form' : about_form,
        'photo_form' : photo_form,
        'resume_form' : resume_form,
        })
