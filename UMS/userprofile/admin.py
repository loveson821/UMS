from django.contrib import admin
from django import forms
from sorl.thumbnail.admin import AdminImageMixin

from .models import UserProfile, Ablum

class AblumAdmin(AdminImageMixin, admin.TabularInline):
    model = Ablum

class UserProfileAdmin(admin.ModelAdmin):
	inlines = [AblumAdmin]

admin.site.register(UserProfile, UserProfileAdmin)