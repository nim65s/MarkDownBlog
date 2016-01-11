from datetime import date

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, RedirectView

from .models import BlogEntry


class BlogEntryMixin(object):
    queryset = BlogEntry.on_site.all()
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
        yea, mon, day = (int(self.kwargs[k]) for k in ['yea', 'mon', 'day'])
        if billet.date != date(yea, mon, day):
            raise Http404
        return billet.get_absolute_url()
