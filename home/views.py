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
from home.models import Area


# Create your views here.
@login_required
def index(request):

	data = {"SA": Course.objects.filter(area=Area.objects.get(code="STL")).values('pk')}
	return render(
   	    request,
        'index.html',
    	data,
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
	# for springcourse in Course.objects.filter(season='s').all():
	# 	allcourses.append(springcourse)
	# for fallcourse in Course.objects.filter(season='f').all():
	# 	allcourses.append(fallcourse)
	# for bothcourse in Course.objects.filter(season='b').all():
	# 	allcourses.append(bothcourse)
	allcourses = Course.objects.all_info()

	# User already exists and plan is NOT blank
	if User.objects.filter(netid=cnetid).count() > 0:
		if User.objects.get(netid=cnetid).plan.saved_courses.all().count() > 0 :
			user = User.objects.get(netid=cnetid)
			plan_courses = user.plan.return_courses()
			courses_by_sem = user.plan.return_by_sem()

			for course in plan_courses:
				if course in all_courses:
					allcourses.remove(course)

			first_info = {'saved': True, 'deg': plan.deg, 'conc': plan.conc, 'concreqs': Concentration.objects.get(name=plan.conc).update_reqs(plan_courses), 
			'degreqs': Concentration.objects.get(name=plan.deg).update_reqs(plan_courses), 'courses': allcourses}
			first_info = first_info.update(courses_by_sem)
		else:
			first_info = {'saved': False, 'courses': allcourses, 'fall1': Course.objects.get(courseid='010097').all_info_solo(), 'fall2': Course.objects.get(courseid='008072').all_info_solo(), 'spring1': Course.objects.get(courseid='007987').all_info_solo(), 'spring2': Course.objects.get(courseid='000976').all_info_solo()}
	#if either no user object or no plans
	else:
		blankplan = Plan()
		blankplan.save()
		u = User(netid=cnetid, plan=blankplan)
		u.save()
		first_info = {'saved': False, 'courses': allcourses, 'fall1': Course.objects.get(courseid='010097').all_info_solo(), 'fall2': Course.objects.get(courseid='008072').all_info_solo(), 'spring1': Course.objects.get(courseid='007987').all_info_solo(), 'spring2': Course.objects.get(courseid='000976').all_info_solo()}
	print (allcourses)
	return render(
		request,
		'schedule.html',
		first_info,
	)
@login_required
def choose_season(request):
	season = request.GET.get('season', None)
	courses = []
	for c in Course.objects.filter(season=season):
		courses.append(c.title)
	data = {'coursesbyseason': courses}
	return JsonResponse(data)

@login_required
def choose_conc(request):
	#also need AB/BSE reqs

	conc_code = request.GET.get('conc', None)
	conc = conc_code[5:len(conc_code)-1]

	conc_o = Concentration.objects.get(name=conc)

	#hardcoded for AB. change later!!!
	degreereqs = Concentration.objects.get(name="A.B.").get_reqs()


	# save deg to associated user plan if user has saved plan
	cnetid = request.user.username
	userplan = User.objects.get(netid=cnetid).plan
	userplan.conc = conc_o
	userplan.save()

	# print(degreereqs)

	data = {'concreqs': conc_o.get_reqs(),
			'degreereqs': degreereqs
	}


	print(data)

	return JsonResponse(data)

@login_required
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

@login_required
def dropped_course(request):
	cid = request.GET.get('id', None)
	term = request.GET.get('term', None)
	season = term[:1]
	year = int(term[-2:])
	course = Course.objects.get(courseid=cid)


	# have to modify when 'both' classes are considered
	# print (course)
	print (course.season)
	print (term)

	allcourses = Course.objects.all_info()
	allowed = False
	if (course.season == season): # Probably have to modify
	 	allowed = True


	data = {'allowed': allowed}
	if allowed:
		#if user already has a plan. NOTE: THIS SHOULD ALWAYS BE TRUE
		if User.objects.filter(netid=request.user.username).count() > 0:		
			plan = User.objects.get(netid=request.user.username).plan

			#add course to plan
			sem = Semester.objects.create(season=season, year=year)
			sem.save()
			s_course = SavedCourse(course=course, semester=sem)
			s_course.save()
			plan.saved_courses.add(s_course)
			#recalculate reqs
			conc = User.objects.get(netid=request.user.username).plan.conc
			conc = User.objects.get(netid=request.user.username).plan.deg
			concreqs = Concentration.objects.get(name=conc).update_reqs(plan.return_courses())
			degreereqs = Concentration.objects.get(name=deg).update_reqs(plan.return_courses())

			#save plan
			plan.save()

			#
			user = User.objects.get(netid=cnetid)
			plan_courses = user.plan.return_courses()
			courses_by_sem = user.plan.return_by_sem()

			for c in plan_courses:
				if c in all_courses:
					print ("here")
					allcourses.remove(c)

			data.update({'concreqs': concreqs, 'degreereqs': degreereqs, 'allcourses': allcourses})

	return JsonResponse(data)

@login_required
def remove_course(request):
	course = request.GET.get('removedcourse', None)

	# return new updated plan
	# return new course list to populate on the side with removed course added


@login_required
def sampleschedules(request):
	return render(
		request,
		'sampleschedules.html',
	)
@login_required
def aas(request):
	return render(
		request,
		'aas.html',
	)
@login_required
def ant(request):
	return render(
		request,
		'ant.html',
	)

@login_required
def arc(request):
	return render(
		request,
		'arc.html',
	)
@login_required
def art(request):
	return render(
		request,
		'art.html',
	)
@login_required
def ast(request):
	return render(
		request,
		'ast.html',
	)	
@login_required	
def cbe(request):
	return render(
		request,
		'cbe.html',
	)
@login_required
def cee(request):
	return render(
		request,
		'cee.html',
	)
@login_required
def chm(request):
	return render(
		request,
		'chm.html',
	)
@login_required
def cla(request):
	return render(
		request,
		'cla.html',
	)
@login_required
def com(request):
	return render(
		request,
		'com.html',
	)
@login_required
def cos(request):
	return render(
		request,
		'cos.html',
	)
@login_required
def eas(request):
	return render(
		request,
		'eas.html',
	)
@login_required
def eco(request):
	return render(
		request,
		'eco.html',
	)
@login_required
def eeb(request):
	return render(
		request,
		'eeb.html',
	)
@login_required
def ele(request):
	return render(
		request,
		'ele.html',
	)
@login_required
def eng(request):
	return render(
		request,
		'eng.html',
	)
@login_required	
def fit(request):
	return render(
		request,
		'fit.html',
	)
@login_required
def geo(request):
	return render(
		request,
		'geo.html',
	)
@login_required
def ger(request):
	return render(
		request,
		'ger.html',
	)
@login_required
def his(request):
	return render(
		request,
		'his.html',
	)
@login_required
def mae(request):
	return render(
		request,
		'mae.html',
	)
@login_required
def mat(request):
	return render(
		request,
		'mat.html',
	)
@login_required	
def mol(request):
	return render(
		request,
		'mol.html',
	)
@login_required
def mus(request):
	return render(
		request,
		'mus.html',
	)
@login_required
def nes(request):
	return render(
		request,
		'nes.html',
	)
@login_required
def neu(request):
	return render(
		request,
		'neu.html',
	)
@login_required
def orf(request):
	return render(
		request,
		'orf.html',
	)
@login_required
def phi(request):
	return render(
		request,
		'phi.html',
	)
@login_required
def phy(request):
	return render(
		request,
		'phy.html',
	)
@login_required
def pol(request):
	return render(
		request,
		'pol.html',
	)
@login_required
def psy(request):
	return render(
		request,
		'psy.html',
	)
@login_required
def rel(request):
	return render(
		request,
		'rel.html',
	)
@login_required
def sla(request):
	return render(
		request,
		'sla.html',
	)
@login_required
def soc(request):
	return render(
		request,
		'soc.html',
	)
@login_required
def spa(request):
	return render(
		request,
		'spa.html',
	)
@login_required
def wws(request):
	return render(
		request,
		'wws.html',
	)
