import os

from django.conf.urls.defaults import *
from django.conf import settings
from django.views.static import serve

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('thaihealthplm.accounts.urls')),
    (r'^', include('thaihealthplm.administration.urls')),
    (r'^', include('thaihealthplm.domain.urls')),
    (r'^', include('thaihealthplm.homepage.urls')),
    (r'^', include('thaihealthplm.budget.urls')),
    (r'^', include('thaihealthplm.kpi.urls')),
    (r'^', include('thaihealthplm.progress.urls')),
    
    (r'^accounts/', include('registration.backends.default.urls')),
    
    (r'^admin/(.*)', admin.site.root),
    
    
    
    
    (r'^$', 'homepage.views.view_homepage'),
    
)

if settings.DEBUG:
    urlpatterns += patterns('', 
        (r'^m/(?P<path>.*)$', serve, {
            'document_root' : os.path.join(os.path.dirname(__file__), "media")
        })
    )