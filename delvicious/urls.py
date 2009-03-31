from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'django.contrib.auth.views.login', {'template_name': 'delvicious/index.html'}),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'delvicious/index.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url': '/delvicious/index.html'}),
    
    (r'^fetch_bookmarks/$', 'delvicious.fetch_bookmarks'),
    (r'^add_delicious_account/$', 'delvicious.views.add_delicious_account'),
    (r'^search/$', 'delvicious.views.search'),
    
    # Override the default registration form
  #  url(r'^account/register/$', 'registration.views.register',
  #     kwargs={'form_class': UserRegistrationForm},
  #     name='registration_register'),
        
)