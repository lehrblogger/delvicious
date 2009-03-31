from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'delvicious.views.list_entries'),
    (r'^sign/$', 'delvicious.views.create_entry'),
    (r'^signup/$', 'delvicious.views.create_new_user'),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'delvicious/user_create_form.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url': '/delvicious/'}),
)