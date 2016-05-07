from datetime import date

from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, RedirectView

from .models import BlogEntry


class BlogEntryMixin(object):
    queryset = BlogEntry.on_site.filter(is_visible=True)
    permanent = True


class BlogEntryListView(BlogEntryMixin, ListView):
    paginate_by = 5


class BlogEntryDetailView(BlogEntryMixin, DetailView):
    pass


class BlogEntryShortURLRedirectView(BlogEntryMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        try:
            pk = int(self.kwargs['pk'], 16)
        except:
            raise Http404
        return get_object_or_404(self.queryset, pk=pk).get_absolute_url()


class BlogEntryLongURLRedirectView(BlogEntryMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        billet = get_object_or_404(self.queryset, slug=self.kwargs['slug'])
        year, month, day = (int(self.kwargs[k]) for k in ['year', 'month', 'day'])
        if billet.date != date(year, month, day):
            raise Http404
        return billet.get_absolute_url()


class CategoryTagDetailView(DetailView):
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['object_list'] = self.object.blogentry_set.filter(is_visible=True, sites=get_current_site(self.request))
        ctx['title'] = '%s: %s' % (self.model._meta.verbose_name, self.object)
        return ctx
