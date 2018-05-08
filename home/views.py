from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from home.models import Concentration
from django.shortcuts import render_to_response
from home.models import Concentration
from home.models import User
from home.models import Course
from home.models import CourseManager

# Create your views here.
@login_required
def index(request):


	test = Concentration.objects.get(name="Chemistry").get_reqs()
	print(test)
	
	# courses = ["010828"]
	# print(Concentration.objects.get(name="Art and Archaeology").update_reqs(courses))

	allconcentrations = []
	for conc in Concentration.objects.all():
		allconcentrations.append(conc.name)
	context = {"concs": allconcentrations}
	return render(
   	    request,
        'index.html',
        context
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
	allcourses = []
	allconcentrations = []
	cnetid = request.user.username
	courseexplanations = []
	coursedescrip = {}

	# if no current user object, make one
	if len(User.objects.filter(netid=cnetid)) > 0:
		plans = User.objects.filter(netid=cnetid).values('plans')
	# retreive user plans
	else:
		u = User(netid=cnetid)
		u.save()
		plans = []

	# fall18, fall19, spring19, spring20 = []
	# for plan in plans:
	# 	for course in plan:
	# 		if course.year == '2018' and course.season == 'f':
	# 			fall18.append(fallcourse)
	# 		if course.year == '2019':
	# 			fall19.append(fallcourse)
	# 	for springcourse in plan.semester.objects.filter(season='S'):
	# 		if springcourse.year == '2019':
	# 			spring19.append(springcourse)
	# 		if springcourse.year == '2020':
	# 			spring20.append(springcourse)

	springcourses = []
	fallcourses = []
	for springcourse in Course.objects.filter(season='s').all():
		springcourses.append(springcourse)
	for fallcourse in Course.objects.filter(season='f').all():
		fallcourses.append(fallcourse)


	for conc in Concentration.objects.all():
		allconcentrations.append(conc.name)

	info = {"fallcourses": fallcourses, "springcourses": springcourses,
	"courses": Course.objects.all_info(), "conclist": allconcentrations}
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
	conc = request.GET.get('conc', None)
	data = {'reqs': Concentration.objects.get(name=conc).get_reqs()}
	return JsonResponse(data)

def choose_deg(request):
	deg = request.GET.get('deg', None)
	concs = []
	for c in Concentration.objects.filter(degree=deg):
		concs.append(c.code_and_name())
	data = {'concs': concs}
	return JsonResponse(data)

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