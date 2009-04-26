from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'django.contrib.auth.views.login', {'template_name': 'delvicious/index.html'}),
    
    (r'^signup/$', 'delvicious.views.create_new_user'),
    (r'^login/$', 'delvicious.views.login_user'),
    #(r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url': '/delvicious/index.html'}),
    
    (r'^fetch_bookmarks/$', 'delvicious.views.fetch_bookmarks'),
    
    (r'^annotations/(?P<username>\w+)\.xml$', 'delvicious.views.serve_xml'),   
    (r'^csespec/(?P<username>\w+)\.xml$', 'delvicious.views.serve_csespec'),
    
    (r'^search/$', 'delvicious.views.search'),
)