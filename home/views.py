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
	dic = {"instance": Concentration.objects.get_BSE('Chemistry')}
	print ("here")
	print (Concentration.objects.get_BSE('Chemistry'))
	return render(
   	    request,
        'index.html',
        dic
    )

def login(request):
	levelone = ['General Chemistry', 'Req']
	leveltwo = [['Integrated Caluculus'], ['course1', 'course2']]
	levelthree = [[['Calculus I', 'Calculus II']], []]
	dic = {'level1': levelone, 'level2': leveltwo, 'level3': levelthree}

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
	allcourses = []
	allconcentrations = []
	cnetid = request.user.username

	# if no current user object, make one
	if len(User.objects.filter(netid=cnetid)) > 0:
		plans = User.objects.filter(netid=cnetid).values('plans')
	# retreive user plans
	else:
		u = User(netid=cnetid)
		u.save()
		plans = []

	for course in Course.objects.all():
		allcourses.append(course.title)

	for conc in Concentration.objects.all():
		allconcentrations.append(conc.name)

	info = {"plans": plans, "courselist": allcourses, "conclist": allconcentrations}



	return render(
		request,
		'schedule.html',
		info
	)