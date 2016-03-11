from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Reward_Group, Reward, Access_Level, Profile, User_Group
from time import strftime

# Create your views here:

# page loaders
@login_required
def main_page(request):
    '''
    loads the main page, only if logged in
    '''
    username = request.user.username
    return render(request, 'reward/main.html', {'username': username})

@login_required
def profile_page(request):
    '''
    profile page loader
    '''
    context = {
        'user_dob' : request.user.profile.date_of_birth.strftime('%Y-%m-%d'),
        'user_act_group' : request.user.profile.active_group,
        'groups' : Reward_Group.objects.filter(users__id = request.user.id),
    }
    return render(request, 'reward/profile.html', context)

def login_page(request):
    '''
    login page loader
    '''
    context = {}
    return render(request, 'reward/login.html', context)



# login/logout view controllers
def logout_request(request):
    '''
    sends a logout signal and redirects to login page
    '''
    logout(request);
    return redirect('login_page')

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
        if check_uname_exist(username):
            err = 'Sorry, that Username is not avaiable.'
            # error text will be renedered by django template
            return render(request, 'reward/register.html', {'error': err})
        new_user = User.objects.create_user(
            username = username,
            password = password,
            email = email
        ) # NOTE: this create call will trigger new_user_setup from models
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

# user profile page views
def update_email(user, email):
    '''
    updates user e-mail, takes a user object and an email
    returns boolean indicating valid e-mail
    '''
    try:
        # only update if a valid email is passed
        validate_email(email)
        user.email = email
        user.save()
        return True
    except ValidationError:
        # send back a boolean for use by the caller function
        return False

def update_dob(user, dob):
    '''
    updates user date of birth, takes a user object and dob
    '''
    user.profile.date_of_birth = dob
    user.profile.save()
    return True

def update_active_group(user, group):
    '''
    updates user current active group, takes a user object and group object
    returns boolean indicating success or failure
    '''
    # check to make sure user is allowed to be in this group
    group = Reward_Group.objects.get(pk=group)
    if group in Reward_Group.objects.filter(users__id = user.id):
        user.profile.active_group = group
        user.profile.save()
        return True
    return False

def update_first_name(user, fname):
    '''
    updates current user first name
    takes a user object and a first name
    '''
    user.first_name = fname
    user.save()
    return True

def update_last_name(user, lname):
    '''
    updates current user last name
    takes a user object and a last name
    '''
    user.last_name = lname
    user.save()
    return True

def profile_update(request):
    '''
    handles a profile update request, determining which fields need update
    '''
    if request.method == 'POST':
        data = request.POST
        user = request.user
        # store all fields and corresponding update functions
        function_dict = {
            'email' : update_email,
            'date_of_birth' : update_dob,
            'active_group' : update_active_group,
            'first_name' : update_first_name,
            'last_name' : update_last_name,
        }
        update_results = {}
        # check over this list to see if the request contains data to update
        for field in function_dict:
            field_value = data[field]
            # make sure field value is not empty
            if field_value:
                # call appropriate update function on the data
                success = function_dict[field](user, field_value)
                # populate response with update results
                update_results[field] = success
    return JsonResponse(update_results)
