from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from allauth.socialaccount.models import SocialAccount
import hashlib

from sorl.thumbnail import ImageField
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
    avator = ImageField(upload_to='user_profile_imgs')
    address = models.CharField(max_length=140, blank=True)
    phone_number = models.CharField(max_length=20)
    role = models.CharField(max_length=3, choices=POSITION_CHOICES, default='nb')
    timezone = models.CharField(max_length=30, choices=TIMEZONES, default='America/Los_Angeles')
 
    def __unicode__(self):
        return "{}'s profile".format(self.user.username)
 
    def get_field_values(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in UserProfile._meta.fields]

    def profile_image_url(self):
        if self.avator:
            return self.avator.url

        fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')
        if len(fb_uid):
            return "http://graph.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)
     
        return "http://www.gravatar.com/avatar/{}?s=100&d=wavatar".format(hashlib.md5(self.user.email).hexdigest())

    # def get_absolute_url(self):
    #     return reverse("npp/nonprofit_detail", kwargs={"slug": self.slug}) 

    class Meta:
        db_table = 'user_profile'

class Ablum(models.Model):
    owner = models.ForeignKey(UserProfile, related_name="ablum")
    image = ImageField(upload_to='user_ablum')

    def get_absolute_url(self):
        return reverse('profile:ablum', kwargs={
            'pk': self.owner.id,
            'ablum_pk': self.id    
        })