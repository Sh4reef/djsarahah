from django import forms


class CheckUsernameForm(forms.Form):
    username = forms.CharField(min_length=1, max_length=40)