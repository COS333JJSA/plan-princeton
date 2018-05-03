from django.db import models

# Create your models here.
class Contact(models.Model):
	tipe = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	email = models.CharField(max_length=200)

	def __str__(self):
		return str(self.name + ", Type: " + self.tipe + ", Email: " + self.email)

class URL(models.Model):
	url = models.CharField(max_length=500)

	def __str__(self):
		return str(self.url)

class Department(models.Model):
	name = models.CharField(max_length=200)
	code = models.CharField(max_length=9)

	def __str__(self):
		return str(self.name)

class Req_ListManager(models.Manager):
	def get_queryset(self):
		return super(ConcentrationManager, self).get_queryset()

	def get_concentration(self, conc):
		return super(ConcentrationManager, self).get_queryset().get(name = conc)

class Req_List(models.Model):
	name = models.CharField(max_length=100)
	max_counted = models.IntegerField(default=1)
	min_needed = models.IntegerField(default=0)
	description = models.CharField(max_length=200, blank=True, null=True)
	explanation = models.TextField(blank=True, null=True)
	double_counting_allowed = models.BooleanField(default=False)
	max_common_with_major = models.IntegerField(null=True, blank=True)
	pdfs_allowed = models.IntegerField(null=True, blank=True)
	completed_by_semester = models.IntegerField(default=8)
	req_lists_inside = models.ManyToManyField('self', blank=True)
	course_list = models.ManyToManyField("Course", blank=True)
	objects = Req_ListManager()

	def __str__(self):
		return str(self.name)

class ConcentrationManager(models.Manager):
	def get_queryset(self):
		return super(ConcentrationManager, self).get_queryset()

	def get_BSE(self, conc):
		reqs = {}
		for req in super(ConcentrationManager, self).get_queryset().get(name=conc).req_lists.get(name='Prerequisites').req_lists_inside.all():
			courses = []
			courses.append(req.min_needed)
			for course in req.course_list.all():
				courses.append(course)
			reqs[req] = courses
			#print (req)
			#for c in req.:
				#print (course)
				#print subreq.course_list
		print (reqs)
			
#Concentration.objects.get(name = 'African American Studies').req_lists.get(name='Prerequisite ').explanation
class Concentration(models.Model):
	tipe = models.CharField(max_length=15)
	name = models.CharField(max_length=200)
	conc_code = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
	degree = models.CharField(max_length=3)
	year = models.IntegerField()
	urls = models.ManyToManyField(URL)
	contacts = models.ManyToManyField(Contact)
	req_lists = models.ManyToManyField(Req_List)
	objects = ConcentrationManager()
	# sample_plans = models.ManyToManyField('Plan')

	def __str__(self):
		return str(self.name)

	def get_description(self):
		return self.req_lists

	# def get_reqs(self):
	# 	fields = []
	# 	for f in self.meta.fields:
	# 		print (f)

class Professor(models.Model):
	uid = models.CharField(max_length=9)
	name = models.CharField(max_length=200)

	def __str__(self):
		return str(self.name)

class Listing(models.Model):
	department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
	number = models.IntegerField()

	def __str__(self):
		return str(self.department) + " " + str(self.number)

class Class(models.Model):
	classnum = models.CharField(max_length=10)
	enroll = models.IntegerField()
	limit = models.IntegerField()
	starttime = models.TimeField()
	section = models.CharField(max_length=4)
	endtime = models.TimeField()
	roomnum = models.CharField(max_length = 15, null=True, blank=True)
	days = models.CharField(max_length=9)
	bldg = models.CharField(max_length=50)

	def __str__(self):
		return str(self.classnum)

class Area(models.Model):
	code = models.CharField(max_length=3)
	name = models.CharField(max_length=100)

	def __str__(self):
		return str(self.code)

class Course(models.Model):
	professor = models.ManyToManyField(Professor)
	title = models.CharField(max_length=200)
	courseid = models.IntegerField()
	listings = models.ManyToManyField(Listing)
	area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True)
	prereqs = models.ManyToManyField('self', blank=True)
	classes = models.ManyToManyField('Class')
	descrip = models.TextField()
	# semesters = models.ManyToField('Semester')

	def __str__(self):
		return str(self.title)

class UserManager(models.Manager):
	def create_user(self, ni):
		user = self.create(netid=ni)
		return user
		
class User(models.Model):
	netid = models.CharField(max_length = 100)
	plans = models.ManyToManyField('Plan')

	objects = UserManager()

class Plan(models.Model):
 	saved_courses = models.ManyToManyField('SavedCourse')

class SavedCourse(models.Model):
	course = models.ManyToManyField('Course')
	semester = models.ManyToManyField('Semester')

class Semester(models.Model):
	seasons = (('S', "Spring"), ('F', "Fall"))
	season = models.CharField(max_length=6, choices=seasons)
	year = models.IntegerField()