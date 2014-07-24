from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.utils import timezone

from braces.views import UserPassesTestMixin, LoginRequiredMixin
from .models import UserProfile, UserProfileForm

class hasAuthorized(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self, user):
        if long(user.profile.id) == long(self.kwargs['pk']):
            return True
        else:
            raise Http404

class profileDetail(LoginRequiredMixin, generic.DetailView):
    model = UserProfile
    template_name = 'profile/detail.html'

class profileEdit(hasAuthorized, UpdateView):
    model = UserProfile
    template_name = 'profile/edit.html'
    form_class = UserProfileForm

    def get_success_url(self):
        return reverse("profile:detail", kwargs={"pk": self.kwargs['pk']}) 

