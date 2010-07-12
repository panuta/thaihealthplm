from django.conf.urls.defaults import *

urlpatterns = patterns('homepage.views',
    
    url(r'^home/$', 'view_dashboard', name='view_dashboard'),
)
