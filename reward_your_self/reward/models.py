from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

class Reward_Group(models.Model):
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

def create_assoc(user, group, invite_status, access_level):
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
    new_assoc.access.add(access_level)
    return new_assoc

def new_user_setup(sender, instance, created, **kwargs):
    '''
    calls associated functions to create a new user's default database values
    '''
    if created:
        new_group = create_default_group(sender, instance, created)
        new_profile = create_profile(sender, instance, created)
        new_access = default_access_level()
        new_assoc = create_assoc(instance, new_group, created, new_access)
        new_profile.active_group = new_group
        new_profile.save()

def new_group_defaults(sender, instance, created, **kwargs):
    '''
    sets up defaults for any newly created group
    such as default list of rewards
    '''
    if created:
        default_reward = Reward(
            group_id = instance,
            reward_name = 'Default Reward!',
            description = 'This default reward comes with every group! Congratulations!',
            point_cost = 20,
            num_redeemed = 0,
        )
        default_reward.save()
        return default_reward

def default_access_level():
    '''
    ensures there is a default access level created
    creates that level if necessary
    returns that access level
    '''
    default_access_list = Access_Level.objects.filter(access_level='default')
    if not default_access_list:
        default_access = Access_Level(
            access_level = 'default'
        )
        default_access.save()
    else:
        default_access = default_access_list[0]
    return default_access

def user_access_level():
    '''
    ensures there is a user access level created
    creates that level if necessary
    returns that access level
    '''
    user_access_list = Access_Level.objects.filter(access_level='User')
    if not user_access_list:
        user_access = Access_Level(
            access_level = 'User'
        )
        user_access.save()
    else:
        user_access = user_access_list[0]
    return user_access
# signal listeners

post_save.connect(new_user_setup, sender=User, dispatch_uid='banana')
post_save.connect(new_group_defaults, sender=Reward_Group, dispatch_uid='habitat')
