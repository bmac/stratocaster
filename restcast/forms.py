from django import forms

class WatchedRecordForm(forms.Form):
    watched = forms.BooleanField(required=False)


class WatchedRecordCreateForm(forms.Form):
    watched = forms.BooleanField(required=True)
    episode_id = forms.IntegerField(required=True)

class PodcastCreateForm(forms.Form):
    link = forms.CharField(required=True)

class SubscriptionForm(forms.Form):
    podcast_id = forms.IntegerField(required=True)
