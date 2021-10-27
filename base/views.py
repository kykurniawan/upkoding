import logging
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from stream_django.enrich import Enrich

from upkoding.activity_feed import feed_manager
from projects.models import Project

log = logging.getLogger(__name__)


def render_template(name, content_type="text/html; charset=utf-8"):
    """
    Just a shortcuts method.
    """
    return TemplateView.as_view(template_name=name, content_type=content_type)

class Index(TemplateView):
    template_name = 'base/index.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['featured_projects'] = Project.objects.featured()
        return data

    def get(self, request):
        if request.GET.get('partial') == 'activities':
            try:
                enricher = Enrich(('actor', 'object', 'target'))
                feed = feed_manager.get_global_challenge_feed()
                activities = feed.get(limit=10)['results']
                enriched = enricher.enrich_aggregated_activities(activities)
                return render(request, 'base/_activities.html', {'activities': enriched})
            except Exception as e:
                return HttpResponse()
        return super().get(request)
