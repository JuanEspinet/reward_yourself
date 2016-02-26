from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

# Create your views here.
def login_page(request):
    context = {}
    return render(request, 'reward/login.html', context)

def login_attempt(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    context = {}
    if user is not None:
        if user.is_active:
            login(request, user)
            return render(request, 'reward/main.html', context)
        else:
            context.error_message = 'This user has been disabled. \
                Please contact us so we can help you figure out why.'
            return render(request, 'reward/login.html', context)
    else:
        return render(request, 'reward/register.hmtl', context)
