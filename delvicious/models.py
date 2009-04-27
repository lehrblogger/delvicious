from google.appengine.ext import db
from ragendja.auth.models import User

class User(User):
	unhashed_password = db.StringProperty()
	last_updated = db.DateTimeProperty()

	def count_bookmarks(self):
		q = Link.all()
		q.filter('username =', self.username)
		return q.count()
	
	def has_bookmarks(self):
		return self.count_bookmarks() > 0

# 
#     def get_username(self):
#     	 return self.username
# 
#     def get_password(self):
#     	 return self.password

class Link(db.Model):
	#user = db.ReferenceProperty(User, collection_name='user_links')
	username = db.StringProperty()
	url = db.StringProperty()
	title = db.StringProperty()

class Tag(db.Model):
	user = db.ReferenceProperty(User, collection_name='user_tags')
	link = db.ReferenceProperty(Link, collection_name='link_tags')
	tag_name = db.StringProperty()
