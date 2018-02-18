from django import forms

class ManageForm(forms.Form):
    name = forms.CharField(max_length=20)
    email = forms.EmailField(required=False)
    notifications = forms.BooleanField(required=False)
    appear_in_search = forms.BooleanField(required=False)
    allow_anonymous_user = forms.BooleanField(required=False)
