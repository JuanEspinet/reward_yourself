from django.db import models
# from django.contrib.auth.models import User TODO: Change user table implementation to this later

# Create your models here.

class Group(models.Model):
    group_name = models.CharField(max_length=200)
    total_points = models.IntegerField(default=0)

    def __str__(self):
        return self.group_name

class Reward(models.Model):
    reward_name = models.CharField(max_length=120)
    description = models.CharField(max_length=500)
    point_cost = models.IntegerField(default=0)
    num_redeemed = models.IntegerField(default=0)
    group_id = models.ForeignKey('Group', on_delete=models.CASCADE)

    def __str__(self):
        return self.reward_name

class Access_Level(models.Model):
    access_level = models.CharField(max_length=200)

    def __str__(self):
        return self.access_level

class User(models.Model):
    username = models.CharField(max_length=200, primary_key=True)
    password = models.CharField(max_length=200)
    e_mail = models.EmailField(max_length=254)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.username

class User_Group(models.Model):
    group_id = models.ForeignKey('Group', on_delete=models.CASCADE)
    access_id = models.ForeignKey('Access_Level', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return 'Group: {0} Access: {1} User: {2}'.format(self.group_id, \
        self.access_id, self.user_id)
