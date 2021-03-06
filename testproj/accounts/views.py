from django.http import Http404
from django.conf import settings
from django.contrib import messages
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _


from braces.views import LoginRequiredMixin

from .models import Profile
from .forms import ProfileUpdateForm


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile.html'

    def get_object(self):
        if not Profile.objects.filter(slug=self.kwargs['slug']).exists():
            raise Http404
        elif self.request.user.profile != Profile.objects.get(slug=self.kwargs['slug']) and not self.request.user.is_staff:
            raise Http404
        return self.get_queryset().get(slug=self.kwargs['slug'])


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/profile_update.html'
    form_class = ProfileUpdateForm

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        messages.success(self.request, _('Profile updated successfully'))
        return reverse_lazy('accounts:profile_detail', kwargs={'slug': self.request.user.profile.slug})
