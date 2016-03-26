from django import forms
from reward.models import Reward

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
        group = request.user.profile.active_group
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
