from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

class Reward_Group(models.Model):
    '''
    table for storing group information, groups consist of one or more users
    '''
    group_name = models.CharField(max_length=200)
    total_points = models.IntegerField(default=0)
    users = models.ManyToManyField(
        User,
        through='User_Group',
    )

    def __str__(self):
        return self.group_name

class Reward(models.Model):
    reward_name = models.CharField(max_length=120)
    description = models.CharField(max_length=500)
    point_cost = models.IntegerField(default=0)
    num_redeemed = models.IntegerField(default=0)
    last_redeem_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    group_id = models.ForeignKey('Reward_Group', on_delete=models.CASCADE)

    def __str__(self):
        return 'Group: {0}, Reward: {1}, Cost: {2}'.format(self.group_id.group_name, self.reward_name, self.point_cost)

class Access_Level(models.Model):
    access_level = models.CharField(max_length=200)

    def __str__(self):
        return self.access_level

class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False, null=True)
    active_group = models.ForeignKey('Reward_Group', related_name='active', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username

class User_Group(models.Model):
    group = models.ForeignKey(Reward_Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access = models.ManyToManyField(Access_Level)
    invite_accepted = models.BooleanField(default=False)

    def __str__(self):
        return 'Group: {0} User: {1}'.format(self.group, self.user)

# signal receivers for automatic setup

def create_default_group(sender, instance, created, **kwargs):
    '''
    creates default group for a new user
    returns the newly created group
    '''
    new_group = Reward_Group(
        group_name = instance.username,
        total_points = 0
    )
    new_group.save()
    return new_group

def create_profile(sender, instance, created, **kwargs):
    '''
    creates default profile association for a new user
    returns the newly created profile
    '''
    new_profile = Profile(
        user = instance,
    )
    new_profile.save()
    return new_profile

def create_assoc(user, group, invite_status):
    '''
    adds membership association for a user with a group
    returns the newly created association
    '''
    new_assoc = User_Group(
        group = group,
        user = user,
        invite_accepted = invite_status,
    )
    new_assoc.save()
    return new_assoc

def new_user_setup(sender, instance, created, **kwargs):
    '''
    calls associated functions to create a new user's default database values
    '''
    if created:
        new_group = create_default_group(sender, instance, created)
        new_profile = create_profile(sender, instance, created)
        new_assoc = create_assoc(instance, new_group, created)

# signal listeners

post_save.connect(new_user_setup, sender=User, dispatch_uid='banana')
