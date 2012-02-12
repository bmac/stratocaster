from django import forms

class WatchedRecordForm(forms.Form):
    watched = forms.BooleanField(required=False)
