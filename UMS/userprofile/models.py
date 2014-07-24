from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django import forms

import pytz
 
class UserProfile(models.Model):
    POSITION_CHOICES = (
        ('nb','New bird'),
        ('ju','Junior'),
        ('se','Senior'),
        ('ma','Manager'),
    )
    TIMEZONES = [(tz, tz) for tz in pytz.all_timezones]

    user = models.OneToOneField(User, related_name='profile')
    address = models.CharField(max_length=140, blank=True)
    phone_number = models.CharField(max_length=20)
    role = models.CharField(max_length=3, choices=POSITION_CHOICES, default='nb')
    timezone = models.CharField(max_length=30, choices=TIMEZONES, default='America/Los_Angeles')
 
    def __unicode__(self):
        return "{}'s profile".format(self.user.username)
 
    def get_field_values(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in UserProfile._meta.fields]

    # def get_absolute_url(self):
    #     return reverse("npp/nonprofit_detail", kwargs={"slug": self.slug}) 

    class Meta:
        db_table = 'user_profile'

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name

        self.fields.keyOrder = [
            'first_name',
            'last_name',
            'address',
            'phone_number',
            'role',
            'timezone'
        ]

    def save(self, *args, **kwargs):
        super(UserProfileForm, self).save(*args, **kwargs)
        self.instance.user.first_name = self.cleaned_data.get('first_name')   
        self.instance.user.last_name = self.cleaned_data.get('last_name')
        self.instance.user.save()

    class Meta:
        model = UserProfile