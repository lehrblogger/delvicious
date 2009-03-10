import cgi, os, base64
from xml.dom.minidom import parse, parseString
from google.appengine.api import urlfetch

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

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
    
    self.redirect('/search')

class Search(webapp.RequestHandler):
  def get(self):
    self.response.out.write('Search page')


class RSSFeedHandler(webapp.RequestHandler):
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
  
    def get(self, testarg):
        bookmarks = self.searchHTTP('memento85', 'ont9oth1ag6foc') #get these later from datastore, they are being irgnored right now
        urls = [bookmark.getAttribute('href').replace( '&', '&amp;') for bookmark in bookmarks]
       
        self.response.headers['Content-Type'] = 'text/xml'
        
        template_vars = {'urls' : urls}
        path = os.path.join(os.path.dirname(__file__), 'annotations.xml')
        
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