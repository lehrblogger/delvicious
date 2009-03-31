from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

def create_new_user(request):
    form = UserCreationForm()
    # if form was submitted, bind form instance.
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user must be active for login to work
            user.is_active = True
            user.put()
            return HttpResponseRedirect('/delvicious/login/')
    return render_to_response('delvicious/user_create_form.html', {'form': form})
    
    
from django.views.generic.list_detail import object_list
from django.views.generic.create_update import create_object
from django.contrib.auth.decorators import login_required
from delvicious.models import Greeting

def list_entries(request):
    return object_list(request, Greeting.all())

@login_required
def create_entry(request):
    # Add username to POST data, so it gets set in the created model
    # You could also use a hidden form field for example, but this is more secure
    request.POST = request.POST.copy()
    request.POST['author'] = str(request.user.key())
    return create_object(request, Greeting, post_save_redirect='/delvicious')