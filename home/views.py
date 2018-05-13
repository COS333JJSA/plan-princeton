import json
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


all_courses = Course.objects.all_info()
# Create your views here.
@login_required
def index(request):
	return render(
   	    request,
        'home.html',
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

<<<<<<< HEAD
	#ignore 'none' courses
	# all_courses = []
	# for springcourse in Course.objects.filter(season='s').all():
	# 	all_courses.append(springcourse)
	# for fallcourse in Course.objects.filter(season='f').all():
	# 	all_courses.append(fallcourse)
	# for bothcourse in Course.objects.filter(season='b').all():
<<<<<<< HEAD
	# 	allcourses.append(bothcourse)
	all_courses = Course.objects.all_info()
=======
	# 	all_courses.append(bothcourse)
	all_courses = Course.objects.all_info()
	temp = True
>>>>>>> 29baddf4a0f852a9ec4ec4d6d790aa406e7a3cc9

	# User already exists
	if User.objects.filter(netid=cnetid).count() > 0:
<<<<<<< HEAD
		if User.objects.get(netid=cnetid).plan.saved_courses.all().count() > 0 :
			user = User.objects.get(netid=cnetid)
			plan = user.plan
			plan_courses = user.plan.return_courses()
			courses_by_sem = user.plan.return_by_sem()

			for course in plan_courses:
				if course in all_courses:
					allcourses.remove(course)


			first_info = {'saved': True, 'deg': plan.degree, 'conc': plan.conc, 'concreqs': Concentration.objects.get(name=plan.conc).update_reqs(plan_courses), 
			'degreqs': Concentration.objects.get(name=plan.degree).get_reqs(), 'courses': all_courses}
			first_info.update(courses_by_sem)

		else:
			first_info = {'saved': False, 'courses': allcourses, 'fall1': Course.objects.get(courseid='010097').all_info_solo(), 'fall2': Course.objects.get(courseid='008072').all_info_solo(), 'spring1': Course.objects.get(courseid='007987').all_info_solo(), 'spring2': Course.objects.get(courseid='000976').all_info_solo()}
	#if either no user object or no plans
=======
		first_info = {'saved': False, 'courses': all_courses}
	# 	#if plan does not exist
	# 	if not User.objects.get(netid=cnetid).plan.exists():
	# 		first_info = {'saved': False, 'courses': all_courses}
	# 		temp = False
	# 	else:
	# 		userplan = User.objects.get(netid=cnetid).plan
	# 		if userplan.conc is None :
	# 			first_info = {'saved': "degree", 'courses': all_courses, 'degree': userplan.degree, 'degreqs': Concentration.objects.get(name=userplan.degree).get_reqs()}
	# 		elif userplan.saved_courses.count() == 0:
	# 			first_info = {'saved': "conc", 'courses': all_courses, 'degree': userplan.degree, 'conc': userplan.conc, 'degreqs': Concentration.objects.get(name=userplan.degree).get_reqs(), 'concreqs': Concentration.objects.get(name=userplan.conc).get_reqs()}
	# 		# Everything saved
	# 		else:
	# 			plan_courses = user.plan.return_courses()
	# 			courses_by_sem = user.plan.return_by_sem()

	# 			for course in plan_courses:
	# 				if course in all_courses:
	# 					print ("REMOVING")
	# 					print (course)
	# 					all_courses.remove(course)

	# 			first_info = {'saved': True, 'deg': userplan.degree, 'conc': userplan.conc, 'concreqs': Concentration.objects.get(name=userplan.conc).update_reqs(plan_courses), 
	# 			'degreqs': Concentration.objects.get(name=userplan.degree).get_reqs(), 'courses': all_courses}
	# 			first_info.update(courses_by_sem)
=======
	# all_courses = Course.objects.all_info()

	# User already exists
	if User.objects.filter(netid=cnetid).exists():
		userplan = User.objects.get(netid=cnetid).plan
		user = User.objects.get(netid=cnetid)
		#if plan does not exist
		if userplan is None:
			first_info = {'saved': False, 'courses': all_courses}
		elif userplan.conc is None:
				first_info = {'saved': "degree", 'courses': all_courses, 'degree': userplan.degree}
		elif userplan.saved_courses.count() == 0:
			print ("no saved courses")
			first_info = {'saved': "conc", 'courses': all_courses, 'degree': userplan.degree}
		else:
			print ("everthing")
			courses_by_sem = user.plan.return_by_sem()
			plan_courses = userplan.return_courses()
			a_courses = all_courses.copy()

			for course in plan_courses:
				if course.courseid in a_courses:
					del a_courses[course.courseid]

			first_info = {'saved': "all", 'degree': userplan.degree, 'courses': a_courses}
			first_info.update(courses_by_sem)
>>>>>>> 8e1adad63bbc2a21bee9bbe1c8c068c2216eca85
	# # New user
>>>>>>> 29baddf4a0f852a9ec4ec4d6d790aa406e7a3cc9
	else:
		u = User(netid=cnetid)
		u.save()
		first_info = {"saved": False, "courses": all_courses}

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
def on_load(request):
	print("backend load func")
	num = int(request.GET.get('num', None))
	userplan = User.objects.get(netid=request.user.username).plan
	plan_courses = userplan.return_courses()

	if num == 1:
		concreqs = []
		conc = ""
	else:
		concreqs = Concentration.objects.get(name=userplan.conc).update_reqs(plan_courses)
		conc = userplan.conc.code_and_name()

	concs = []
	for c in Concentration.objects.filter(degree=userplan.degree):
		if c.name != "AB" and c.name != "BSE":
			concs.append(c.code_and_name())

	print(conc)

	data = {'concreqs': concreqs, 'degreqs': Concentration.objects.get(name=userplan.degree).update_reqs(plan_courses), 
	'concs': concs, 'conc': conc}
	return JsonResponse(data)

@login_required
def choose_conc(request):
	# get argument
	conc_code = request.GET.get('conc', None)
	print(conc_code)

	# get user plan
	cnetid = request.user.username
	userplan = User.objects.get(netid=cnetid).plan
	plan_courses = userplan.return_courses()

	# if default then set to None
	if conc_code == "Select Concentration:":
		userplan.conc = None
		concreqs = []
	else:
		#parse conc code
		paren = conc_code.index('(')
		conc = conc_code[paren+1:len(conc_code)-1]
		# set conc
		userplan.conc = Concentration.objects.get(name=conc)
		concreqs = Concentration.objects.get(name=userplan.conc).update_reqs(plan_courses)

	# save plan
	userplan.save()

	#calculate degreqs
	degreereqs = Concentration.objects.get(name=userplan.degree).update_reqs(plan_courses)

	data = {'concreqs': concreqs, 'degreereqs': degreereqs}

	return JsonResponse(data)

@login_required
def choose_deg(request):

	#get data from frontend
	deg = request.GET.get('deg', None).upper()

	cnetid = request.user.username

	# if user.plan is null, create plan
	user = User.objects.get(netid=cnetid)
	if user.plan is None:
		plan = Plan(degree=deg)
		plan.save()
		user.plan = plan
		user.save()
	else:
		plan = user.plan
		plan.degree = deg
		user.plan = plan
		plan.save()
	

	#send frontend list of concs associated with deg	
	concs = []
	for c in Concentration.objects.filter(degree=deg):
		if c.name != "AB" and c.name != "BSE":
			concs.append(c.code_and_name())
	data = {'concs': concs}

	return JsonResponse(data)

@login_required
def dropped_course(request):
<<<<<<< HEAD
<<<<<<< HEAD


	course = request.GET.get('course', None)
	chosensemester = request.GET.get('chosensemester', None)
	year = ""
	allowed = false
	if (course.season == chosensemester): # Probably have to modify
		allowed = true

=======
=======

>>>>>>> 8e1adad63bbc2a21bee9bbe1c8c068c2216eca85
	#get and parse data from front end
>>>>>>> 29baddf4a0f852a9ec4ec4d6d790aa406e7a3cc9
	cid = request.GET.get('id', None)
	term = request.GET.get('term', None)
	season = term[:1]
	year = int(term[-2:])
	course = Course.objects.get(courseid=cid)
	user = User.objects.get(netid=request.user.username)


<<<<<<< HEAD
	cnetid = request.user.username
	userplan = User.objects.get(netid=cnetid).plan
	# usercourses = userplan.return_courses


=======
	#determine if course is allowed in this semester
>>>>>>> 29baddf4a0f852a9ec4ec4d6d790aa406e7a3cc9
	allcourses = Course.objects.all_info()
	allowed = False
	if (course.season == season) or (course.season == 'b'): # Probably have to modify
		allowed = True

	print(course.title)
	data = {'allowed': allowed}
	print (course.season)
	print (allowed)
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
			degreereqs = Concentration.objects.get(name=degree).update_reqs(plan.return_courses())
			#save plan
			plan.save()
			data.update({'concreqs': concreqs, 'degreereqs': degreereqs})


			plan_courses = plan.return_courses()
			courses_by_sem = user.plan.return_by_sem()

			for c in plan_courses:
				if c in allcourses:
					allcourses.remove(c)

			print("returning")

			data.update({'concreqs': concreqs, 'degreereqs': degreereqs, 'allcourses': allcourses})

	return JsonResponse(data)

@login_required
def send_sample(request):
	plans = Concentration.objects.get(conc_code="CHM").sample_plans
	
	if len(plans) == 0:
		return

	return plans[0].return_by_sem()



@login_required
def remove_course(request):
	print("hi")
	cid = request.GET.get('course', None)
	course = Course.objects.get(courseid=cid)

	cnetid = request.user.username
	user = User.objects.get(netid=cnetid)
	plan = user.plan

	# remove course from plan
	for c in plan.saved_courses.all():
		if c.course.courseid == cid:
			plan.saved_courses.remove(c)

	# remove plan courses from all courses
	# plan_courses = plan.return_courses()
	# a_courses = all_courses.copy()

	# for course in plan_courses:
	# 	if course.courseid in a_courses:
	# 		del a_courses[course.courseid]

	# data = {"courses": a_courses, 'concreqs': Concentration.objects.get(name=plan.conc).update_reqs(plan_courses), 'degreqs': Concentration.objects.get(name=plan.degree).update_reqs(plan_courses)}
	return JsonResponse(data = {"msg": "hi"})

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
