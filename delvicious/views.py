from django.contrib.auth.models import User
import base64
from xml.dom.minidom import parse, parseString
from django.contrib.auth import authenticate, login
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import check_password

from django.views.generic.list_detail import object_list
from django.views.generic.create_update import create_object
from django.shortcuts import render_to_response
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import Context, loader


from google.appengine.api import users, urlfetch
from google.appengine.ext import db

from delvicious.forms import UserCreationForm, UserLoginForm
from delvicious.models import User, Link


def serve_csespec(request, username):
	q = User.all()
	q.filter('username =', username)
	if q.count() > 0:
		return render_to_response('delvicious/csespec.xml', {'username': username})
	
def serve_xml(request, username):
	q = User.all()
	q.filter('username =', username)
	if q.count() > 0:
		return render_to_response('delvicious/annotations.xml', {'links': Link.gql("WHERE username = :1 ", username), 'username': username})

def create_new_user(request):
    form = UserCreationForm()
    # if form was submitted, bind form instance.
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
			user = form.save()
			user.is_active = True
			user.put()
			#TODO Authenticate first?
			#login(request, user)
			return HttpResponseRedirect('/delvicious/')
    return render_to_response('delvicious/user_create_form.html', {'form': form})

def login_user(request):
    form = UserLoginForm()
    # if form was submitted, bind form instance.
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
			user = authenticate(username=request.POST['username'], password=request.POST['password'])
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect('/delvicious/')
    return render_to_response('delvicious/user_login_form.html', {'form': form})
 
def main(request):
	curuser = request.user
	#return render_to_response('delvicious/text.html', {'text': curuser.has_bookmarks()})
	return render_to_response('delvicious/index.html', {'user': curuser})

@login_required
def fetch_bookmarks(request):
	curuser = request.user
	#curuser = users.get_current_user()
	if curuser.is_authenticated():
		bookmarks = search_http(curuser.username, curuser.unhashed_password)
		if len(bookmarks) > 0:
			for bookmark in bookmarks:
				query =  Link.all()
				query.filter('username =', curuser.username)
				query.filter('url =', bookmark.getAttribute('href').replace('&', '&amp;'))
				if not query:
					b = Link()
					b.username = curuser.username
					b.url = bookmark.getAttribute('href').replace('&', '&amp;')
					b.title = bookmark.getAttribute('description')
					b.put()
			#return render_to_response('delvicious/link_list.html', {'object_list': Link.all()})		
			return HttpResponseRedirect('/delvicious/')
		else:
			return render_to_response('delvicious/text.html', {'text': 'no bookmarks for ' + curuser.username + ' with password=' + curuser.unhashed_password + '___'})
	else:
		return render_to_response('delvicious/text.html', {'text': 'no user'})

def search_http(username, password):
	res = urlfetch.fetch('https://api.del.icio.us/v1/posts/all', 
 						 headers={'Authorization': 'Basic ' + base64.b64encode(username + ":" + password)},
 						 allow_truncated=True)
	#res = urlfetch.fetch('http://lehrblogger.com/nyu/classes/spring09/a2z/midterm/testing.xml')
	if res.content.find('Sorry, Unable to process request at this time -- error 999.') != -1:
		return #TODO make this work? render_to_response('delvicious/text.html', {'text': 'rate limit hit for ' + curuser.username})
	else:
		dom = parseString(res.content.partition('<!--')[0])
		return dom.getElementsByTagName('post')
