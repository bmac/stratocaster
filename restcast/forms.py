from django import forms

class WatchedRecordForm(forms.Form):
    watched = forms.BooleanField(required=False)


class WatchedRecordCreateForm(forms.Form):
    watched = forms.BooleanField(required=True)
    episode_id = forms.IntegerField(required=True)
