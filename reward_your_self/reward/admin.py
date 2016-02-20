from django.contrib import admin
from .models import Group, User, Reward, User_Group, Access_Level
# Register your models here.
admin.site.register(Group)
admin.site.register(User)
admin.site.register(Reward)
admin.site.register(User_Group)
admin.site.register(Access_Level)
