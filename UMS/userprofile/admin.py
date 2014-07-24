from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import UserProfile

# class UserProfileAdmin(admin.ModelAdmin):
admin.site.register(UserProfile)