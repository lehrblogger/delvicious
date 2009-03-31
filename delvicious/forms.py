# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from django.utils.translation import ugettext_lazy as _, ugettext as __
from ragendja.auth.models import UserTraits
from ragendja.forms import FormWithSets, FormSetField
from registration.forms import RegistrationForm, RegistrationFormUniqueEmail
from registration.models import RegistrationProfile
from google.appengine.api import users


from delvicious.models import DeliciousAccount



class AddDeliciousAccountForm(forms.ModelForm):
    username = forms.RegexField(regex=r'^\w+$', max_length=30,
        label=_(u'Username'))
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False),
        label=_(u'Password'))
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False),
        label=_(u'Password (again)'))

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already in use.
        
        """
        new_delicious_account = DeliciousAccount.get_by_key_name("key_"+self.cleaned_data['username'].lower())
        if new_delicious_account:# and new_delicious_account.is_active:
            raise forms.ValidationError(__(u'That Delicious account is already associated with this Google account. Please choose another.'))
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
        
        new_delicious_account = DeliciousAccount(username=self.cleaned_data['username'], password=self.cleaned_data['password1'])
        #new_delicious_account = DeliciousAccount(user = users.get_current_user(), username=self.cleaned_data['username'], password=self.cleaned_data['password1'])
      #  self.instance = new_delicious_account
        return new_delicious_account
#        return super(UserRegistrationForm, self).save()