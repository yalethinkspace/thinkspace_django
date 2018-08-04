from django.contrib.auth import login, authenticate
from django.shortcuts import render, HttpResponse, redirect

from client.forms import SignUpForm

def index(request):
    return render(request, "index.html")

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponse("logged in")
    else:
        form = SignUpForm()
    return render(request, 'registration/sign-up.html', {'form': form})
