from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import DateTimeInput
from safe.models import UserAttributes, Safe


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')


class UserAttributeForm(forms.ModelForm):
    class Meta():
        model = UserAttributes
        fields = ('displayname',)


class SafeUpdateForm(forms.ModelForm):
    PROXIMITY_CHOICES = [
        ('M', 'Minutes'),
        ('H', 'Hours'),
        ('D', 'Days'),
        ('W', 'Weeks')
    ]
    auth_to_unlock = forms.BooleanField()
    unlock_time = forms.DateTimeInput(attrs={'class': 'datetime-input'})
    scanfreq = forms.IntegerField()
    reportfreq = forms.IntegerField
    proximityunit = forms.ChoiceField(choices=PROXIMITY_CHOICES)
    displayproximity = forms.BooleanField()
    keyholder_msg = forms.TextInput()

    class Meta():
        model = Safe
        fields = ('auth_to_unlock', 'unlock_time', 'scanfreq', 'reportfreq', 'proximityunit',
                  'displayproximity', 'keyholder_msg')