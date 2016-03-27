from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Reward_Group, Reward, Access_Level, Profile, User_Group
from time import strftime
from .forms import Reward_Form

# Create your views here:

# page loaders
@login_required
def main_page(request):
    '''
    loads the main page, only if logged in
    '''
    user_groups = User_Group.objects.filter(user=request.user.id)
    active_group = request.user.profile.active_group
    group_rewards = Reward.objects.filter(group_id=active_group)
    highest_avail = get_high_avail(group_rewards, active_group.total_points)
    next_avail = get_next_highest(group_rewards, highest_avail.point_cost)
    context = {
        'user_groups' : user_groups,
        'highest_avail' : highest_avail,
        'next_avail' : next_avail,
        'active_group' : active_group,
    }
    return render(request, 'reward/main.html', context)

@login_required
def profile_page(request):
    '''
    profile page loader
    '''
    context = {
        'user_dob' : request.user.profile.date_of_birth.strftime('%Y-%d'),
        'user_act_group' : request.user.profile.active_group,
        'groups' : Reward_Group.objects.filter(users__id = request.user.id),
    }
    return render(request, 'reward/profile.html', context)

@login_required
def reward_page(request):
    '''
    reward page loader
    '''
    new_reward = Reward_Form(request=request)
    context = {
        'rewards' : Reward.objects.filter(group_id=request.user.profile.active_group.id),
        'rew_form' : new_reward
    }
    return render(request, 'reward/rewards.html', context)

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

# main page views
def reward_available(reward, total):
    '''
    compares a reward's point value to the total
    and determines if the user can afford that reward
    '''
    if reward.point_cost <= total:
        return reward
    return False

def check_highest(highest, current):
    '''
    checks two reward point costs and returns whichever is the highest
    current can be a reward object or boolean
    highest must be a reward object
    returns existing highest if the two values are equal
    '''
    if current and highest.point_cost < current.point_cost:
        return current
    return highest

def check_lowest(lowest, current):
    '''
    checks two reward point costs and determines which is lowest
    current can be a reward object or boolean
    lowest must be a reward object
    returns existing lowest if the two values are equal
    '''
    if current and lowest.point_cost > current.point_cost:
        return current
    return lowest

def get_high_avail(rewards, total_points):
    '''
    compares a list of rewards to total points and returns
    the highest cost reward the user can afford
    '''
    highest = rewards[0]
    for reward in rewards:
        highest = check_highest(highest, reward_available(reward, total_points))
    return highest

def get_next_highest(rewards, total_points):
    '''
    compares a list of rewards and finds the next reward
    costing higher than the current point total
    '''
    lowest = False
    for reward in rewards:
        if not reward_available(reward, total_points):
            if not lowest:
                lowest = reward
            lowest = check_lowest(lowest, reward)
    return lowest

def add_point(request):
    '''
    processes an add point click from a user
    '''
    if request.method == 'GET':
        request.user.profile.active_group.point_total += 1
    return HttpResponseRedirect('/main/')

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

# reward page views
def deduct_points(group, points):
    '''
    deducts points from a group
    usually for redeeming a reward
    '''
    if group.total_points < points:
        return 'Not enough points.'
    group.total_points -= points
    group.save()
    return group.total_points

def update_redeemed(reward):
    '''
    increments the number of times a reward has been redeemed
    returns the reward object
    '''
    reward.num_redeemed += 1
    reward.save()
    return reward

def new_reward(request):
    '''
    processes form submittal for adding a new reward to a group
    '''
    if request.method == 'POST':
        form = Reward_Form(request.POST, request=request)
        if form.is_valid():
            form.save()
            request.POST = {}
    return HttpResponseRedirect('/rewards/')

def redeem_reward(request):
    '''
    processes a user redeeming a reward for a group
    '''
    if request.method == 'POST':
        # find the right group to take the points from
        group = request.user.profile.active_group
        # find the right reward to mark as redeemed
        reward = Reward.objects.get(id=request.POST['reward_id'])
        # change group's point total
        new_total = deduct_points(group, reward.point_cost)
        # update number of times this reward redeemed
        reward = update_redeemed(reward)
        return JsonResponse({'new_total' : new_total})
    return JsonResponse({'new_total': False})
