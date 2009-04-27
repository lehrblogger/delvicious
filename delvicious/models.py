from google.appengine.ext import db
from ragendja.auth.models import User

class User(User):
    last_updated = db.DateTimeProperty()
    
    def has_bookmarks(self):
    	q = Link.all()
    	#q.filter("WHERE user = :1 ", self)
    	return q.count() > 0
# 
#     def get_username(self):
#     	 return self.username
# 
#     def get_password(self):
#     	 return self.password

class Link(db.Model):
	#user = db.ReferenceProperty(User, collection_name='user_links')
	user = db.UserProperty()
	url = db.StringProperty()
	title = db.StringProperty()

class Tag(db.Model):
	user = db.ReferenceProperty(User, collection_name='user_tags')
	link = db.ReferenceProperty(Link, collection_name='link_tags')
	tag_name = db.StringProperty()
