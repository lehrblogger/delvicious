import cgi, os, base64
from xml.dom.minidom import parse, parseString
from google.appengine.api import urlfetch

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
  
def addDeliciousAccount(self):
	user = users.get_current_user()
	
    if user:
AddDeliciousAccountForm
    else:
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write('user fail on addDeliciousAccount')
      #self.redirect(users.create_login_url(self.request.uri))



addDeliciousAccount