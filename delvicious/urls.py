from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'django.contrib.auth.views.login', {'template_name': 'delvicious/index.html'}),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'delvicious/index.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url': '/delvicious/index.html'}),
    
    (r'^fetch_bookmarks/$', 'delvicious.views.fetch_bookmarks'),
    (r'^add_delicious_account/$', 'delvicious.views.add_delicious_account'),
    (r'^search/$', 'delvicious.views.search'),
    (r'^annotations/(?P<username>\w+)\.xml$', 'delvicious.views.serveXML'),
    
    # Override the default registration form
  #  url(r'^account/register/$', 'registration.views.register',
  #     kwargs={'form_class': UserRegistrationForm},
  #     name='registration_register'),
        
)

#delv-icio-us.appspot.com/annotations/memento85.xml