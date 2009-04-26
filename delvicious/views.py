from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from delvicious.forms import UserCreationForm

from django.views.generic.list_detail import object_list
from django.views.generic.create_update import create_object
from django.contrib.auth.decorators import login_required

from google.appengine.ext import db
from delvicious.models import DeliciousAccount, Link

from google.appengine.api import users


def serve_csespec(request, username):
	daccounts = DeliciousAccount.gql("WHERE username = :1 ", username)
	for curdaccounts in daccounts:
		return render_to_response('delvicious/csespec.html', {'username': username})
		
	return render_to_response('delvicious/text.html', {'text': curuser.user})
	
def serve_xml(request, username):
	daccounts = DeliciousAccount.gql("WHERE username = :1 ", username)
	for curdaccounts in daccounts:
		return render_to_response('delvicious/annotations.html', {'links': Link.gql("WHERE user = :1 ", curdaccounts.user), 'username': username})
		
	return render_to_response('delvicious/text.html', {'text': curuser.user})

#maybe not two of this line?
@login_required
def fetch_bookmarks(request):
	curuser = users.get_current_user()
	if curuser:
		delicious_login = DeliciousAccount.gql("WHERE user = :user", user=curuser).get()
		if delicious_login:
			bookmarks = searchHTTP(delicious_login.username, delicious_login.password)
			for bookmark in bookmarks:
				query =  Link.all()
				query.filter('user =', curuser)
				query.filter('url =', bookmark.getAttribute('href').replace('&', '&amp;'))
				if not query:
					b = Link(user = curuser)
					b.url = bookmark.getAttribute('href').replace('&', '&amp;')
					b.title = bookmark.getAttribute('description')
					b.put()
			return render_to_response('delvicious/link_user.html', {'user': curuser, 'links': Link.gql("WHERE user = :1 ", curuser)})
		else:
			return render_to_response('delvicious/text.html', {'text': 'no delicious user'})
	else:
		return render_to_response('delvicious/text.html', {'text': 'no user'})


import base64
from google.appengine.api import urlfetch
from xml.dom.minidom import parse, parseString
def searchHTTP (username, password):
	res = urlfetch.fetch('https://api.del.icio.us/v1/posts/all', 
 						 headers={'Authorization': 'Basic ' + base64.b64encode(username + ":" + password)},
 						 allow_truncated=True)
#	res = urlfetch.fetch('http://lehrblogger.com/nyu/classes/spring09/a2z/midterm/testing.xml')
	if res.content.find('Sorry, Unable to process request at this time -- error 999.') != -1:
		return
	else:
		dom = parseString(res.content.partition('<!--')[0])
		return dom.getElementsByTagName('post')
		
		
		
		

def create_new_user(request):
    form = UserCreationForm()
    # if form was submitted, bind form instance.
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # user must be active for login to work
            user.is_active = True
            user.put()
            return HttpResponseRedirect('/delvicious/login/')
    return render_to_response('delvicious/user_create_form.html', {'form': form})
    
    

    
#@login_required
def search(request):
	curuser = users.get_current_user()
	if curuser:
		delicious_login = DeliciousAccount.gql("WHERE user = :user", user=curuser).get()
		if delicious_login:
			return render_to_response('delvicious/search.html', {'username': delicious_login.username})
		else:
			return render_to_response('delvicious/text.html', {'text': 'no delicious user'})
	else:
		return render_to_response('delvicious/text.html', {'text': 'no user'})
