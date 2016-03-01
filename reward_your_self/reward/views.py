from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here:
@login_required
def main_page(request):
    username = request.user.username
    return render(request, 'reward/main.html', {'username': username})

def logout_request(request):
    logout(request);
    return redirect('login_page')



def login_page(request):
    '''
    login page loader
    '''
    context = {}
    return render(request, 'reward/login.html', context)

def login_attempt(request):
    '''
    attempts a login, sends to register if user does not exist yet
    '''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        context = {
            'username': username
        }
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'reward/main.html', context)
            else:
                context.error_message = 'This user has been disabled. \
                    Please contact us so we can help you figure out why.'
                return render(request, 'reward/login.html', context)
        else:
            return render(request, 'reward/register.html', context)

def register_attempt(request):
    '''
    attempts to register a new user
    '''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        date_of_birth = request.POST['date_of_birth']
        if check_uname_exist(username):
            err = 'Sorry, that Username is not avaiable.'
            return render(request, 'reward/register.html', {'error': err})
        new_user = User.objects.create_user(
            username = username,
            password = password,
            email = email
        )
        return login_attempt(request)

def check_uname_exist(username):
    '''
    takes a username and returns a boolean indicating if that username exists
    '''
    try:
        User.objects.get(username__iexact=username)
    except User.DoesNotExist:
        return False
    return True
