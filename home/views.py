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

	print(Course.objects.filter(area=Area.objects.get(code="SA")).values('pk'))
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

	#dep = Department.objects.get(=conc_code)


	# if (Concentration.objects.get(conc_code=dep).degree == 'AB'):
	# 	degreereqs = Concentration.objects.get(name='AB').get_reqs()
	# else:
	# 	degreereqs = Concentration.objects.get(name='BSE').get_reqs()
	degreereqs = ['Degree Reqs will be Here!']


	# save deg to associated user plan if user has saved plan
	cnetid = request.user.username
	userplan = User.objects.get(netid=cnetid).plan
	userplan.conc = Concentration.objects.get(name=conc)
	userplan.save()



	data = {'concreqs': Concentration.objects.get(name=conc).get_reqs(),
			'degreereqs': degreereqs
	}
	print("hi")
	print(data)
	return JsonResponse(data)

@login_required
def choose_deg(request):

	#get data from frontend
	deg = request.GET.get('deg', None).upper()
	print(deg)

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
	print(data)
	return JsonResponse(data)

@login_required
def dropped_course(request):
	id = request.GET.get('id', None)
	print(request.GET.get('term', None))
	print(id)
	#print(term)
	course = Course.objects.get(id=id)

	# chosensemester = request.GET.get('chosensemester', None)
	year = ""
	chosensem
	allowed = False
	if (course.season == chosensemester): # Probably have to modify
	 	allowed = True

	data = {'allowed': allowed}
	if allowed:
		#if user already has a plan. NOTE: THIS SHOULD ALWAYS BE TRUE
		if User.objects.filter(netid=request.user.username).count() > 0:		
			plan = User.objects.get(netid=request.user.username).plan

			#add course to plan
			sem = Semester.objects.create(season=chosensemester, year=year)
			sem.save()
			s_course = SavedCourse.objects.create(course=course, semester=sem)
			s_course.save()
			plan.saved_courses.add(s_course)
			#recalculate reqs
			conc = User.objects.get(netid=request.user.username).plan.conc
			conc = User.objects.get(netid=request.user.username).plan.deg
			concreqs = Concentration.objects.get(name=conc).update_reqs(plan.return_courses())
			degreereqs = Concentration.objects.get(name=deg).update_reqs(plan.return_courses())

			#save plan
			plan.save()
			data.update({'concreqs': concreqs, 'degreereqs': degreereqs})

	print (data)
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
