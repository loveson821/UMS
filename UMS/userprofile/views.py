from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.utils import timezone

from braces.views import UserPassesTestMixin, LoginRequiredMixin, JSONResponseMixin, AjaxResponseMixin, CsrfExemptMixin
from .models import UserProfile, Ablum
from .form import UserProfileForm, UploaderForm

class hasAuthorized(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self, user):
        if long(user.profile.id) == long(self.kwargs['pk']):
            return True
        else:
            raise Http404

class profileDetail(LoginRequiredMixin, generic.DetailView):
    model = UserProfile
    template_name = 'profile/detail.html'

    def get_context_data(self, **kwargs):
        context = super(profileDetail, self).get_context_data(**kwargs)
        context['ablum'] = self.object.ablum.all()
        return context

class profileEdit(hasAuthorized, UpdateView):
    model = UserProfile
    template_name = 'profile/edit.html'
    form_class = UserProfileForm

    def get_success_url(self):
        return reverse("profile:detail", kwargs={"pk": self.kwargs['pk']}) 

    def get_context_data(self, **kwargs):
        context = super(profileEdit, self).get_context_data(**kwargs)
        context['ablum'] = self.object.ablum.all()
        return context

class profileAblum(JSONResponseMixin, AjaxResponseMixin, generic.View):
    def get_ajax(self, request, *args, **kwargs):
        json_dict = {
            'Hello': "World"
        }
        return self.render_json_response(json_dict)

    def post_ajax(self, request, *args, **kwargs):
        if request.POST['_method'] == 'DELETE':
            return self.delete_ajax(request, *args, **kwargs)

        form = UploaderForm(request.POST, request.FILES)
        if form.is_valid():
            upload = Ablum(
                owner=request.user.profile,
                image=request.FILES['upload']
            )
            upload.save()
        else:
            errors_dict = {}
            if form.errors:
                for error in form.errors:
                    e = form.errors[error]
                    errors_dict[error] = unicode(e)
                return self.render_json_response(errors_dict)

        return self.render_json_response({'success': True})

    def delete_ajax(self, request, *args, **kwargs):
        profile = get_object_or_404(UserProfile, pk=kwargs['pk'])
        ablum = get_object_or_404(profile.ablum, pk=kwargs['ablum_pk'])
        if request.user.profile != profile:
            raise Http404
        else:
            ablum.delete()
            return self.render_json_response({
                'success': True    
            })

