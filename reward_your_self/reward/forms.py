from django import forms
from reward.models import Reward, Reward_Group, User_Group, create_assoc

class Reward_Form(forms.ModelForm):
    '''
    form for adding new rewards to a group
    '''

    def __init__(self, *args, **kwargs):
        # add request info so it can be accessed later by overridden save method
        self.request = kwargs.pop('request')
        super(Reward_Form, self).__init__(*args, **kwargs)

    def save(self, force_insert=False, force_update=False, commit=True):
        # save method is overridden to allow calculated fields
        new_reward = super(Reward_Form, self).save(commit=False)
        new_reward.num_redeemed = 0
        # retrieve the current user's group from the request
        group = self.request.user.profile.active_group
        new_reward.group_id = group
        if commit:
            new_reward.save()
        return new_reward

    class Meta:
        model = Reward
        fields = [
            'reward_name',
            'description',
            'point_cost',
        ]

class Group_Form(forms.ModelForm):
    '''
    form for maintaining and adding groups
    '''

    def __init__(self, *args, **kwargs):
        # add request info so it can be accessed later by overridden save method
        self.request = kwargs.pop('request')
        super(Group_Form, self).__init__(*args, **kwargs)

    def save(self, force_insert=False, force_update=False, commit=True):
        # save method is overridden to allow calculated fields
        new_group = super(Group_Form, self).save(commit=False)
        new_group.total_points = 0
        # retrieve the current user from the request
        user = self.request.user
        if commit:
            new_group.save()
            # create the association between creating user and group
            new_assoc = User_Group(
                group = new_group,
                user = user,
                invite_accepted = True,
            )
            new_assoc.save()
        return new_group


    class Meta:
        model = Reward_Group
        fields = [
            'group_name',
        ]
