# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('challenge.views',
                       (r'^$', 'list_challenges'),
                       (r'^create_challenge/$', 'add_challenge'),
                       (r'^show_challenge/(?P<id>.+)$', 'show_challenge'),
)
