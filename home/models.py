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
	code = models.CharField(max_length=3)

	def __str__(self):
		return str(self.name)

class Req_List(models.Model):
	name = models.CharField(max_length=100)
	max_counted = models.IntegerField(default=1)
	min_needed = models.IntegerField(default=0)
	description = models.CharField(max_length=200, blank=True)
	explanation = models.TextField()
	double_counting_allowed = models.BooleanField(default=False)
	max_common_with_major = models.IntegerField(null=True, blank=True)
	pdfs_allowed = models.IntegerField(null=True, blank=True)
	completed_by_semester = models.IntegerField(default=8)
	req_lists_inside = models.ManyToManyField('self', blank=True)
	course_list = models.ManyToManyField("Course")


	def __str__(self):
		return str(self.name)

class Concentration(models.Model):
	tipe = models.CharField(max_length=15)
	name = models.CharField(max_length=200)
	conc_code = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
	degree = models.CharField(max_length=3)
	year = models.IntegerField()
	urls = models.ManyToManyField(URL)
	contacts = models.ManyToManyField(Contact)
	req_lists = models.ManyToManyField(Req_List)


	def __str__(self):
		return str(self.name)

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
	roomnum = models.IntegerField(null=True)
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

	def __str__(self):
		return str(self.title)



 #class User(models.Model):
 	# userid = models.AutoField()
 	# username = models.CharField(max_length = 100)
 	# password = ??
 	# past_courses = models.ManyToManyField(Course)
 	# past_APs = AP model?
#enrollment
#save templates