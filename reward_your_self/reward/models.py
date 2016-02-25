from django.db import models
from django.contrib.auth.models import User

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
    group_id = models.ForeignKey('Reward_Group', on_delete=models.CASCADE)

    def __str__(self):
        return self.reward_name

class Access_Level(models.Model):
    access_level = models.CharField(max_length=200)

    def __str__(self):
        return self.access_level

class Reward_User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False)
    groups = models.ManyToManyField(
        Reward_Group,
        through='User_Group',
    )
    # TODO add active_group foreign key to reward_group

    def __str__(self):
        return self.username

class User_Group(models.Model):
    group_id = models.ForeignKey('Reward_Group', on_delete=models.CASCADE)
    user_id = models.ForeignKey('Reward_User', on_delete=models.CASCADE)
    access_id = models.ManyToManyField(Access_Level)
    invite_accepted = models.BooleanField(default=False)

    def __str__(self):
        return 'Group: {0} Access: {1} User: {2}'.format(self.group_id, \
        self.access_id, self.user_id)
