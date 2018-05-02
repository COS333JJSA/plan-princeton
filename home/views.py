from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from home.models import Concentration
from django.shortcuts import render_to_response

# Create your views here.
@login_required
def index(request):
	#instance = Concentration.objects.get_BSE('Chemistry')
	instance = {"hi": "julieto", "hello": "julieto"}
	return render(
   	    request,
        'index.html',
         instance,
    )


def login(request):
	return render(
		request,
		'login.html',
	)

@login_required
def scheduler(request):
	return render(
		request,
		'schedule.html'
	)

