from django import forms

class PodcastCreateForm(forms.Form):
    link = forms.CharField(required=True)
