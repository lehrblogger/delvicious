import cgi
import base64
from xml.dom.minidom import parse, parseString
from google.appengine.api import urlfetch

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


class DelviciousUser(db.Model):
  gaccount = db.UserProperty()
  daccount = db.StringProperty(multiline=False)
  dpassword = db.StringProperty(multiline=False)
  date = db.DateTimeProperty(auto_now_add=True)

class FrontPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write('<html><body>')

    self.response.out.write("""
          <form action="/register" method="post">
            <div><input name="daccount" rows="1" cols="60"></input></div>
            <div><input name="dpassword" rows="1" cols="60"></input></div>
            <div><input type="submit" value="Register"></div>
          </form>""")
      
    self.response.out.write('</html></body>')

class Register(webapp.RequestHandler):
  def post(self):
    delviciousUser = DelviciousUser()

    if users.get_current_user():
      delviciousUser.gaccount = users.get_current_user()

    delviciousUser.daccount = self.request.get('daccount')
    delviciousUser.dpassword = self.request.get('dpassword')
    delviciousUser.put()
    
    #updateObj = Updater()
    #updateObj.updateAnnotations(self.request.get('daccount'), self.request.get('dpassword'))
    
    self.redirect('/search')

class Search(webapp.RequestHandler):
  def post(self):
    print 'Content-Type: text/plain'
    print ''
    print 'Hello, world!'


class RSSFeedHandler(webapp.RequestHandler):
    def searchHTTP (self, username, password):
        #url = 'https://' + username + ':' + password + '@api.del.icio.us/v1/posts/all'
        #url = 'http://lehrblogger.com/nyu/classes/spring09/a2z/midterm/testing.xml'
        url = 'https://memento85:ont9oth1ag6foc@api.del.icio.us/v1/posts/all'
    
        #unpw = base64.b64encode("memento85:ont9oth1ag6foc")'
        res = urlfetch.fetch('https://api.del.icio.us/v1/posts/all', 
                         headers={'Authorization': 'Basic ' + base64.b64encode("memento85:ont9oth1ag6foc")},
                         allow_truncated=True)
        res = urlfetch.fetch('http://lehrblogger.com/nyu/classes/spring09/a2z/midterm/testing.xml')                 
        print res.content
        dom = parseString(res.content.partition('<!--')[0])
        return dom.getElementsByTagName('post')
  
    def get(self):
        bookmarks = self.searchHTTP('memento85', 'ont9oth1ag6foc') #get these later from datastore, they are being irgnored right now
        self.response.headers['Content-Type'] = 'text/xml'

        template_vars = {'bookmarks' : articles}
        path = os.path.join(os.path.dirname(__file__), self.get_template('annotations.xml'))

        self.response.out.write(template.render(path, template_vars))





application = webapp.WSGIApplication(
                                     [('/', FrontPage),
                                      ('/register', Register),
                                      ('/search', Search),
                                      ('/annotations/(.*)', RSSFeedHandler)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()