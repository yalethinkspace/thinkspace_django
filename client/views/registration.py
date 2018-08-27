# IMPORTS

# response
from django.shortcuts import render, HttpResponse, redirect
# models
from client.models import *
# forms
from client.forms import *
# mailing
from django.core.mail import send_mail # send emails
from django.template.loader import render_to_string # render emails
# tokens
from client.tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# in-built login utils
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
# signals
from django.contrib.auth.signals import user_logged_in, user_logged_out
# decorators
from django.dispatch import receiver
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET, require_http_methods
# flash messages
from django.contrib import messages
# other
from django.contrib.sites.shortcuts import get_current_site

# VIEWS

# login and logout views are implemented via django.contrib.auth in urls.py

# sign up with email confirmation
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid(): # validate form input as it was specified
            user = form.save(commit=False) # save new user but don't commit to db yet
            user.is_active = False # mark the user as inactive - they can't sign in yet
            user.save() # save user to db
            current_site = get_current_site(request) # retrieve domain name
            # render email message; pass in params to template
            subject = 'Welcome to Thinkspaces. Please activate your account.'
            message = render_to_string('email/account_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            send_mail(subject, message, 'noreply@thinkspaces.org', [user.email]) # send template email to user
            # add success message to flash queue
            messages.success(request, 'Your account has been created. Please check your email for a link to verify your account.')
            return redirect('index') # redirect to home page
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
@login_required(login_url='/users/login/')
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
    return redirect('dashboard_profile')