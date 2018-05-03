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










