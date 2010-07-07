import os

from django.conf.urls.defaults import *
from django.conf import settings
from django.views.static import serve

from django.contrib import admin
admin.autodiscover()

from homepage.views import view_homepage

urlpatterns = patterns('',
    #(r'^', include('thaihealthsms.accounts.urls')),
    #(r'^', include('thaihealthsms.domain.urls')),
    #(r'^', include('thaihealthsms.budget.urls')),
    #(r'^', include('thaihealthsms.kpi.urls')),
    #(r'^', include('thaihealthsms.progress.urls')),
    
    (r'^accounts/', include('registration.backends.default.urls')),
    
    (r'^admin/(.*)', admin.site.root),
    
    (r'^$', view_homepage),
)

if settings.DEBUG:
    urlpatterns += patterns('', 
        (r'^m/(?P<path>.*)$', serve, {
            'document_root' : os.path.join(os.path.dirname(__file__), "media")
        })
    )