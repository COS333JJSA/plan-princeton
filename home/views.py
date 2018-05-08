from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from home.models import Concentration
from django.shortcuts import render_to_response
from home.models import Concentration
from home.models import User
from home.models import Course
from home.models import CourseManager
from django.http import JsonResponse
from home.models import Plan

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
def scheduler(request):
	cnetid = request.user.username
	first_info = {}

	#ignore 'none' courses
	allcourses = []
	for springcourse in Course.objects.filter(season='s').all():
		allcourses.append(springcourse)
	for fallcourse in Course.objects.filter(season='f').all():
		allcourses.append(fallcourse)
	for bothcourse in Course.objects.filter(season='b').all():
		allcourses.append(bothcourse)

	#if user object exists and saved plan exists, load saved
	# if User.objects.filter(netid=cnetid).count() > 0 and Plan.objects.filter(netid=cnetid).count() > 0:
	# 	plan = User.objects.filter(netid=cnetid).values('plan')
	# 	plan_courses = plan.return_courses()
	
	# 	first_info = {'saved': True, 'deg': plan.deg, 'conc': plan.conc, 'concreqs': Concentration.objects.get(name=plan.conc).update_reqs(plan_courses), 
	# 	'degreqs': Concentration.objects.get(name=plan.deg).update_reqs(plan_courses)}
	# #if either no user object or no plans
	# else:
		# if no current user object, make one
		if User.objects.filter(netid=cnetid).count() == 0:
			u = User(netid=cnetid)
			u.save()
		first_info = {'saved': False}

	info = {"courses": allcourses}

	return render(
		request,
		'schedule.html',
		info
	)

def choose_season(request):
	season = request.GET.get('season', None)
	courses = []
	for c in Course.objects.filter(season=season):
		courses.append(c.title)
	data = {'coursesbyseason': courses}
	return JsonResponse(data)

def choose_conc(request):
	#also need AB/BSE reqs
	print ("hi")
	conc = request.GET.get('conc', None)
	if (conc.degree == 'AB'):
		degreereqs = Concentration.objects.get(name='AB').get_reqs()
	else:
		degreereqs = Concentration.objects.get(name='BSE').get_reqs()

	#save deg to associated user plan
	cnetid = request.user.username
	plan = User.objects.filter(netid=cnetid).values('plan')
	plan.conc = Concentration.objects.get(name=conc)
	plan.save()

	data = {'concreqs': Concentration.objects.get(name=conc).get_reqs(),
			'degreereqs': degreereqs
	}
	return JsonResponse(data)

def choose_deg(request):
	#get data from frontend
	deg = request.GET.get('deg', None).upper()

	#save deg to associated user plan
	cnetid = request.user.username
	plan = User.objects.filter(netid=cnetid).values('plan')
	plan.degree = deg
	# plan.save()

	#send frontend list of concs associated with deg	
	concs = []
	for c in Concentration.objects.filter(degree=deg):
		concs.append(c.code_and_name())
	data = {'concs': concs}

	return JsonResponse(data)

def dropped_course(request):
	course = request.GET.get('course', None)
	chosensemester = request.GET.get('chosensemester', None)
	allowed = false
	if (course.season == chosensemester): # Probably have to modify
		allowed = true
	data = {'allowed': allowed}
	return JsonResponse(data)

def remove_course(request):
	course = request.GET.get('removedcourse', None)

def sampleschedules(request):
	return render(
		request,
		'sampleschedules.html',
	)
def aas(request):
	return render(
		request,
		'aas.html',
	)
def ant(request):
	return render(
		request,
		'ant.html',
	)
def arc(request):
	return render(
		request,
		'arc.html',
	)
def art(request):
	return render(
		request,
		'art.html',
	)
def ast(request):
	return render(
		request,
		'ast.html',
	)		
def cbe(request):
	return render(
		request,
		'cbe.html',
	)
def cee(request):
	return render(
		request,
		'cee.html',
	)
def chm(request):
	return render(
		request,
		'chm.html',
	)
def cla(request):
	return render(
		request,
		'cla.html',
	)
def com(request):
	return render(
		request,
		'com.html',
	)
def cos(request):
	return render(
		request,
		'cos.html',
	)
def eas(request):
	return render(
		request,
		'eas.html',
	)
def eco(request):
	return render(
		request,
		'eco.html',
	)
def eeb(request):
	return render(
		request,
		'eeb.html',
	)
def ele(request):
	return render(
		request,
		'ele.html',
	)
def eng(request):
	return render(
		request,
		'eng.html',
	)	
def fit(request):
	return render(
		request,
		'fit.html',
	)
def geo(request):
	return render(
		request,
		'geo.html',
	)
def ger(request):
	return render(
		request,
		'ger.html',
	)
def his(request):
	return render(
		request,
		'his.html',
	)
def mae(request):
	return render(
		request,
		'mae.html',
	)
def mat(request):
	return render(
		request,
		'mat.html',
	)	
def mol(request):
	return render(
		request,
		'mol.html',
	)
def mus(request):
	return render(
		request,
		'mus.html',
	)
def nes(request):
	return render(
		request,
		'nes.html',
	)
def neu(request):
	return render(
		request,
		'neu.html',
	)
def orf(request):
	return render(
		request,
		'orf.html',
	)
def phi(request):
	return render(
		request,
		'phi.html',
	)
def phy(request):
	return render(
		request,
		'phy.html',
	)
def pol(request):
	return render(
		request,
		'pol.html',
	)
def psy(request):
	return render(
		request,
		'psy.html',
	)
def rel(request):
	return render(
		request,
		'rel.html',
	)
def sla(request):
	return render(
		request,
		'sla.html',
	)
def soc(request):
	return render(
		request,
		'soc.html',
	)
def spa(request):
	return render(
		request,
		'spa.html',
	)
def wws(request):
	return render(
		request,
		'wws.html',
	)