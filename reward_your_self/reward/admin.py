from django.contrib import admin
from .models import Reward_Group, Reward_User, Reward, User_Group, Access_Level
# Register your models here.
admin.site.register(Reward_Group)
admin.site.register(Reward_User)
admin.site.register(Reward)
admin.site.register(User_Group)
admin.site.register(Access_Level)
