# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('challenge.views',
                       (r'^$', 'list_challenges'),
                       (r'^create_challenge/$', 'add_challenge'),
                       (r'^show_challenge/(?P<id>.+)$', 'show_challenge'),
                       (r'^(?P<challenge_id>.+)/reporter/(?P<reporter_id>.+)/sparkline_url$', 'spark_line'),
                       (r'^(?P<challenge_id>.+)/reporter/(?P<reporter_id>.+)', 'list_reports' ),
)
