from django.urls import reverse
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.dispatch import receiver
from django.contrib import messages
from client.forms import *

# email
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from client.tokens import account_activation_token
from django.utils.encoding import force_text

# pagination
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# models
from client.models import User, Message, Conversation, Post

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
            send_mail(subject, message, 'noreply@thinkspaces.org', [user.email])
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

# render dashboard
@login_required(login_url='/users/login/')
def dashboard(request):
    return render(request, 'dashboard/layout.html')

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


@login_required(login_url='/users/login/')
def dashboard_profile(request):
    if request.method == 'POST':
        print(request.POST)
        # deal with multiple forms
        # HTML form names must be distinct from the data trying to be saved by
        # the form (as below with the _form suffix), otherwise it will coalesce
        # with the form name and save empty
        if 'photo_form' in request.POST:
            form = DashboardPhotoForm(request.POST, instance=request.user)
        if 'about_form' in request.POST:
            form = DashboardAboutForm(request.POST, instance=request.user)
        if 'basic_info_form' in request.POST:
            form = DashboardBasicInfoForm(request.POST, instance=request.user)
        if 'resume_form' in request.POST:
            form = DashboardResumeForm(request.POST, instance=request.user)
        # check form validity and save 
        if form.is_valid():
            form.save()
            print(form)
            messages.success(request, 'Your information was successfully changed.')
        else:
            messages.error(request, 'Your information could not be changed. Please correct any errors.')
        return redirect('dashboard_profile')
    else:
        password_change_form = PasswordChangeForm(request.user)
        basic_info_form = DashboardBasicInfoForm(instance=request.user)
        about_form = DashboardAboutForm(instance=request.user)
        photo_form = DashboardPhotoForm(instance=request.user)
        resume_form = DashboardResumeForm(instance=request.user)
    return render(request, 'dashboard/profile.html', {
        'password_change_form': password_change_form,
        'basic_info_form': basic_info_form,
        'about_form': about_form,
        'photo_form': photo_form,
        'resume_form': resume_form,
    })


@login_required(login_url='/users/login/')
def dashboard_settings(request):
    if request.method == 'POST':
        # deal with multiple forms
        # HTML form names must be distinct from the data trying to be saved by
        # the form (as below with the _form suffix), otherwise it will coalesce
        # with the form name and save empty
        if 'delete_form' in request.POST:
            try:
                request.user.delete()
                messages.success(request, "Your account was deleted.")
            except Exception as e:
                messages.error(request, "Something went wrong. Your account could not be deleted.")
        return redirect('index')
    return render(request, 'dashboard/settings.html')

@login_required(login_url='/users/login/')
def dashboard_messages_conversation_list(request):
    conversations = request.user.conversations.all()
    return render(request, 'dashboard/messages/conversation_list.html', 
    {
        "conversations" : conversations,
    })

@login_required(login_url='/users/login/')
def dashboard_messages_conversation(request, conversation_id):
    conversation = Conversation.objects.get(pk=conversation_id)
    if request.method == 'POST':
        # check if message form was sent
        if 'message_form' in request.POST:
            # prepare the missing fields
            initial_message = Message.objects.create(
                conversation=conversation,
                sender=request.user
            )
            form = DashboardMessageForm(request.POST, instance=initial_message)
        # save message to database
        if form.is_valid():
            form.save()
        else:
            messages.error(
                request, 'Your message could not be sent, please try again.')
            # update unread count in conversation
            conversation.their_unread_count += 1
            conversation.save()
            # compute the number of unseen messages
            
        # redirect back to the conversation
        return redirect('dashboard_messages_conversation', conversation_id)
    else:
        # prepare a message form for render
        message_form = DashboardMessageForm()
        # mark all unread messages in the conversation as read
        # unread_messages = conversation.messages.filter(is_unread=True)
        # for message in unread_messages.all():
        #     message.is_unread = False
        #     message.save()
        conversation.my_unread_count = 0
        conversation.save()
    return render(request, 'dashboard/messages/conversation.html', {
        "conversation" : conversation,
        "message_form" : message_form,
    })

def news(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 1)  # show 5 posts per page
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'news/news_list.html', {
        "posts" : posts,
    })

def news_item(request, post_id):
    post = Post.objects.get(pk=post_id)
    return render(request, 'news/news_item.html', {
        "post" : post,
    })
