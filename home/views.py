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
from home.models import SavedCourse
from home.models import Semester
from home.models import Department
# from signal import signal, SIGPIPE, SIG_DFL
# signal(SIGPIPE, SIG_DFL)

# Create your views here.

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


def logout(request):
	return render(
		request,
		'login.html',
	)


def scheduler(request):
	cnetid = request.user.username
	first_info = {}

	#ignore 'none' courses
	# all_courses = []
	# for springcourse in Course.objects.filter(season='s').all():
	# 	all_courses.append(springcourse)
	# for fallcourse in Course.objects.filter(season='f').all():
	# 	all_courses.append(fallcourse)
	# for bothcourse in Course.objects.filter(season='b').all():
	# 	all_courses.append(bothcourse)
	all_courses = Course.objects.all_info()

	# User already exists and plan is NOT blank
	if User.objects.filter(netid=cnetid).count() > 0:
		if User.objects.get(netid=cnetid).plan.saved_courses.all().count() > 0 :
			user = User.objects.get(netid=cnetid)
			plan = user.plan
			plan_courses = user.plan.return_courses()
			courses_by_sem = user.plan.return_by_sem()

			for course in plan_courses:
				if course in all_courses:
					all_courses.remove(course)

			first_info = {'saved': True, 'deg': plan.degree, 'conc': plan.conc, 'concreqs': Concentration.objects.get(name=plan.conc).update_reqs(plan_courses), 
			'degreqs': Concentration.objects.get(name=plan.degree).get_reqs(), 'courses': all_courses}
			first_info.update(courses_by_sem)


		else:
			first_info = {'saved': False, 'courses': all_courses}
	#if either no user object or no plans
	else:
		blankplan = Plan()
		blankplan.save()
		u = User(netid=cnetid, plan=blankplan)
		u.save()
		first_info = {"saved": False, "courses": all_courses}

	return render(
		request,
		'schedule.html',
		first_info,
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

	conc_code = request.GET.get('conc', None)
	conc = conc_code[5:len(conc_code)-1]


	# save deg to associated user plan if user has saved plan
	cnetid = request.user.username
	userplan = User.objects.get(netid=cnetid).plan
	userplan.conc = Concentration.objects.get(name=conc)
	userplan.save()

	degreereqs = Concentration.objects.get(userplan.conc).get_reqs()



	data = {'concreqs': Concentration.objects.get(name=conc).get_reqs(),
			'degreereqs': degreereqs
	}
	return JsonResponse(data)


def choose_deg(request):

	#get data from frontend
	deg = request.GET.get('deg', None).upper()

	#save deg to associated user plan
	cnetid = request.user.username
	userplan = User.objects.get(netid=cnetid).plan
	userplan.degree = deg
	userplan.save()
	#print (User.objects.get(netid=cnetid).plan.degree)

	#send frontend list of concs associated with deg	
	concs = []
	for c in Concentration.objects.filter(degree=deg):
		concs.append(c.code_and_name())
	data = {'concs': concs}

	return JsonResponse(data)


def dropped_course(request):
	#get and parse data from front end
	cid = request.GET.get('id', None)
	term = request.GET.get('term', None)
	season = term[:1]
	year = int(term[-2:])
	course = Course.objects.get(courseid=cid)
	user = User.objects.get(netid=request.user.username)


	#determine if course is allowed in this semester
	allcourses = Course.objects.all_info()
	allowed = True
	# if (course.season == season): # Probably have to modify
	#  	allowed = True

	data = {'allowed': allowed}
	#if course is allowed in the semester, update plan and recalculate reqs
	if allowed:
		#if user already has a plan. NOTE: THIS SHOULD ALWAYS BE TRUE
		if user.plan is not None:		
			plan = user.plan

			#add course to plan
			sem = Semester.objects.create(season=season, year=year)
			sem.save()
			s_course = SavedCourse.objects.create(course=course, semester=sem)
			s_course.save()
			plan.saved_courses.add(s_course)
			#recalculate reqs
			conc = User.objects.get(netid=request.user.username).plan.conc
			degree = User.objects.get(netid=request.user.username).plan.degree
			concreqs = Concentration.objects.get(name=conc).update_reqs(plan.return_courses())
			# degreereqs = Concentration.objects.get(name=degree).update_reqs(plan.return_courses())
			degreereqs = Concentration.objects.get(name=degree).get_reqs()
			#save plan
			plan.save()
			data.update({'concreqs': concreqs, 'degreereqs': degreereqs})


			plan_courses = plan.return_courses()
			courses_by_sem = user.plan.return_by_sem()

			for c in plan_courses:
				if c in allcourses:
					allcourses.remove(c)

			data.update({'concreqs': concreqs, 'degreereqs': degreereqs, 'allcourses': allcourses})

	return JsonResponse(data)


def remove_course(request):
	course = request.GET.get('removedcourse', None)

	# return new updated plan
	# return new course list to populate on the side with removed course added



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
