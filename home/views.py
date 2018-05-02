from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):

	return render(
   	    request,
        'index.html',
    )

def login(request):
	return render(
		request,
		'login.html',
	)

@login_required
def logout(request):
	return render(
		request,
		'login.html',
	)

@login_required
def schedule(request):
	# cnetid = request.user.username
	# #if no current user object, make one
	# if len(User.objects.filter(netid=cnetid)) > 0:
	# 	plans = User.objects.filter(netid=cnetid).values('plans')
	# #retreive user plans
	# else:

	return render(
		request,
		'schedule.html'
	)