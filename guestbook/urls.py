from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'guestbook.views.list_entries'),
    (r'^sign/$', 'guestbook.views.create_entry'),
    (r'^signup/$', 'guestbook.views.create_new_user'),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'guestbook/user_create_form.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url': '/guestbook/'}),
)