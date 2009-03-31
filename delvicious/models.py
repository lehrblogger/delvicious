from google.appengine.ext import db
from django.contrib.auth.models import User

class DeliciousAccount(db.Model):
	#user = db.ReferenceProperty(User)
	username = db.StringProperty()
	password = db.StringProperty()

class Link(db.Model):
	user = db.ReferenceProperty(User, collection_name='user_links')
	url = db.StringProperty()
	title = db.StringProperty()

class Tag(db.Model):
	user = db.ReferenceProperty(User, collection_name='user_tags')
	link = db.ReferenceProperty(Link, collection_name='link_tags')
	tag_name = db.StringProperty()
