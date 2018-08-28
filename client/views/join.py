# IMPORTS

# response
from django.shortcuts import render, HttpResponse, redirect

# VIEWS
def join(request):
    return render(request, 'join/join.html')

def newsletter(request):
    return redirect('join')