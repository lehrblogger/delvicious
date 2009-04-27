import base64

from datetime import datetime
from xml.dom.minidom import parse, parseString
from registration.forms import RegistrationForm, RegistrationFormUniqueEmail
from registration.models import RegistrationProfile

from django import forms
from django.core.files.uploadedfile import UploadedFile
from django.utils.translation import ugettext_lazy as _, ugettext as __
#from django.contrib.auth.models import User

from ragendja.auth.models import UserTraits
from ragendja.forms import FormWithSets, FormSetField

from google.appengine.api import users, urlfetch
from delvicious.models import User



class UserLoginForm(forms.ModelForm):
	username = forms.RegexField(regex=r'^\w+$', max_length=30,
		label=_(u'Delicious username'))
	password = forms.CharField(widget=forms.PasswordInput(render_value=False),
		label=_(u'Delicious password'))
		
	def clean_username(self):
		"""
		Validate that the username is in use.
		
		"""
		user = User.gql("WHERE username = :1 ", self.cleaned_data['username'])
		if not user:
			raise forms.ValidationError(__(u'That is not a valid username.'))
		return self.cleaned_data['username']

class UserCreationForm(forms.ModelForm):
	username = forms.RegexField(regex=r'^\w+$', max_length=30,
		label=_(u'Username'))
	password1 = forms.CharField(widget=forms.PasswordInput(render_value=False),
		label=_(u'Password'))
	password2 = forms.CharField(widget=forms.PasswordInput(render_value=False),
		label=_(u'Password (again)'))
	email = forms.EmailField(label=_(u'Email address'))
	
	last_updated = datetime.now() #TODO make sure this is changing from now
	
	def clean_username(self):
		"""
		Validate that the username is alphanumeric and is not already in use.
		
		"""
		q = User.all()
		q.filter('user =', self.cleaned_data['username'].lower())
		
		if q.count() > 0:
			raise forms.ValidationError(__(u'That Delicious account is already signed up for Delvicious. Please login or choose another.'))
		return self.cleaned_data['username']

	def clean(self):
		"""
		Verifiy that the values entered into the two password fields
		match. Note that an error here will end up in
		``non_field_errors()`` because it doesn't apply to a single
		field.
		
		"""
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
			if self.cleaned_data['password1'] != self.cleaned_data['password2']:
				raise forms.ValidationError(__(u'You must type the same password each time'))
				
		if 'username' in self.cleaned_data and 'password1' in self.cleaned_data and 'password2' in self.cleaned_data and 'email' in self.cleaned_data:
			temp_username = self.cleaned_data['username'] #'memento85'
			temp_password = self.cleaned_data['password1'] #'ont9oth1ag6foc'
			res = urlfetch.fetch('https://api.del.icio.us/v1/posts/update', 
 						 headers={'Authorization': 'Basic ' + base64.b64encode(temp_username+ ":" + temp_password)},
 						 allow_truncated=True)
			dom = parseString(res.content.partition('<!--')[0])
			nodes = dom.getElementsByTagName('update')
			if nodes.length > 0:
				self.last_updated = datetime.strptime(nodes[0].getAttribute('time'), "%Y-%m-%dT%H:%M:%SZ")
			else:
				raise forms.ValidationError(__(res.content))
		#https://memento85:ont9oth1ag6foc@api.del.icio.us/v1/posts/update
		#https://memento85:ont9oth1ag6foc@api.del.icio.us/v1/posts/all
		return self.cleaned_data
	
	def save(self, domain_override=""):
		"""
		Create the new ``User`` and ``RegistrationProfile``, and
		returns the ``User``.
		
		This is essentially a light wrapper around
		``RegistrationProfile.objects.create_inactive_user()``,
		feeding it the form data and a profile callback (see the
		documentation on ``create_inactive_user()`` for details) if
		supplied.
		
		"""
		new_user = User.objects.create_user(self.cleaned_data['username'], self.cleaned_data['email'], self.cleaned_data['password1'])
		new_user.unhashed_password = self.cleaned_data['password1']
		new_user.last_updated = self.last_updated
		return new_user