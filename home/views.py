from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from home.models import Concentration
from django.shortcuts import render_to_response
from home.models import Concentration
from home.models import User
from home.models import Course

# Create your views here.
@login_required
def index(request):
	# reqs = Concentration.objects.get_BSE('Chemistry')
	# level_one = []
	# level_two = []
	# level_three = []
	# level_four = []
	# level_one_nums = []
	# counter = 0

	# for r in reqs:
	# 	if type(r) == int:
	# 		if counter % 2 == 0:
	# 			level_one.append(r)
	# 		else:
	# 			level_one_nums.append(r)
	# 		counter += 1
	# 	else:
	# 		for r2 in r:
	# 			if type(r) == int:
	# 				level_two.append(r2)
	# 			else:
	# 				for r3 in r:
	# 					if type(r) == int:
	# 						level_three.append(r3)
	# 					else:
	# 						for r4 in r:
	# 							level_four.append(r4)

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
def scheduler(request):
	cnetid = request.user.username

	#if no current user object, make one
	if len(User.objects.filter(netid=cnetid)) > 0:
		plans = User.objects.filter(netid=cnetid).values('plans')
	#retreive user plans
	else:
		u = User(netid=cnetid)
		u.save()
		plans = []

	info = {"plans": plans}

	return render(
		request,
		'schedule.html',
		info
	)