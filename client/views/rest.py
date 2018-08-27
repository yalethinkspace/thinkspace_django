# IMPORTS

# response
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
# models
from client.models import *
# forms
from client.forms import *
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
from django.urls import reverse

# VIEWS

# render home page
def index(request):
    return render(request, "index.html")

# render dashboard
@login_required(login_url='/users/login/')
def dashboard(request):
    return render(request, 'dashboard/layout.html')

# dashboard profile
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


# dashboard settings
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

