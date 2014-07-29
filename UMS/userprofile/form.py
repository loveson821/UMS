from django.conf import settings
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .models import UserProfile, Ablum

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
            'avator',
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

class UploaderForm(forms.Form):
    """
    Uploader Form
    """
    upload  = forms.FileField()

    def clean_upload(self):
        upload = self.cleaned_data['upload']
        content_type = upload.content_type
        if content_type in settings.CONTENT_TYPES:
            if upload._size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s')\
                       % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(upload._size)))
        else:
            raise forms.ValidationError(_('File type is not supported'))

        return upload