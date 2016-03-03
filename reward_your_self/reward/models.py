from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

class Reward_Group(models.Model):
    group_name = models.CharField(max_length=200)
    total_points = models.IntegerField(default=0)

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
        return self.reward_name

class Access_Level(models.Model):
    access_level = models.CharField(max_length=200)

    def __str__(self):
        return self.access_level

class Reward_User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False, null=True)
    groups = models.ManyToManyField(
        Reward_Group,
        through='User_Group',
    )

    def get_default_group(self):
        return self.groups[0]

    active_group = models.ForeignKey('Reward_Group', related_name='active', on_delete=models.SET(get_default_group), null=True)

    def __str__(self):
        return self.user.username

class User_Group(models.Model):
    group_assoc = models.ForeignKey('Reward_Group', on_delete=models.CASCADE)
    user_assoc = models.ForeignKey('Reward_User', on_delete=models.CASCADE)
    access_assoc = models.ManyToManyField(Access_Level)
    invite_accepted = models.BooleanField(default=False)

    def __str__(self):
        return 'Group: {0} User: {1}'.format(self.group_assoc, self.user_id)

# signal handlers for automatic setup

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
    new_profile = Reward_User(
        user = instance,
    )
    new_profile.save()
    return new_profile

def create_assoc(user_id, group_id):
    '''
    adds membership and access association for a user with a group
    returns the newly created association
    '''
    new_assoc = User_Group(
        group_assoc = group_id,
        user_assoc = user_id,
        invite_accepted = True,
    )
    new_assoc.save()
    return new_assoc

def new_user_setup(sender, instance, created, **kwargs):
    '''
    calls associated functions to create a new user's default database values
    '''
    new_group = create_default_group(sender, instance, created)
    new_profile = create_profile(sender, instance, created)
    new_assoc = create_assoc(new_profile, new_group)

post_save.connect(new_user_setup, sender=User)
