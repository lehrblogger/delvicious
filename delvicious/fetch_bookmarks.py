import cgi, os, base64
from xml.dom.minidom import parse, parseString
from google.appengine.api import urlfetch

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from delvicious.models import DeliciousAccount

def searchHTTP (self, username, password):
	res = urlfetch.fetch('https://api.del.icio.us/v1/posts/all', 
 						 headers={'Authorization': 'Basic ' + base64.b64encode(username + ":" + password)},
 						 allow_truncated=True)
        #res = urlfetch.fetch('http://lehrblogger.com/nyu/classes/spring09/a2z/midterm/testing.xml')
	if res.content.find('Sorry, Unable to process request at this time -- error 999.') != -1:
		print res.content
		print '<br><br><br><br><br>YAHOO API FAIL<br><br><br><br><br>'
	else:
		dom = parseString(res.content.partition('<!--')[0])
		return dom.getElementsByTagName('post')


def getBookmarksAndStore(self):
	user = users.get_current_user()
	
	if user:
		delicious_login = DeliciousAccount.gql("WHERE user = :user", user=users.get_current_user())
	
		return render_to_response('delvicious/user_create_form.html', {'form': form})
		if delicious_login:
			#bookmarks = self.searchHTTP(delicious_login.username, delicious_login.password)
			#for bookmark in bookmarks
				#put in datastore
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.out.write('Hello, ' + user.nickname())
		else:
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.out.write('delicious_login fail')
	else:
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write('user fail')
      #self.redirect(users.create_login_url(self.request.uri))



def get(self, testarg):
	bookmarks = self.searchHTTP('memento85', 'ont9oth1ag6foc') #get these later from datastore
	urls = [bookmark.getAttribute('href').replace( '&', '&amp;') for bookmark in bookmarks]
       
	self.response.headers['Content-Type'] = 'text/xml'
        
	template_vars = {'urls' : urls}
	path = os.path.join(os.path.dirname(__file__), 'annotations.xml')
        
	self.response.out.write(template.render(path, template_vars))



getBookmarksAndStore

