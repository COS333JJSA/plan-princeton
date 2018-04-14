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
		return self.url

class Department(models.Model):
	name = models.CharField(max_length=200)
	code = models.CharField(max_length=3)

	def __str__(self):
		return self.name

class Req_List(models.Model):
	name = models.CharField(max_length=100)
	max_counted = models.IntegerField()
	min_needed = models.IntegerField()
	description = models.CharField(max_length=200)
	explanation = models.TextField()
	double_counting_allowed = models.BooleanField()
	max_common_with_major = models.IntegerField()
	pdfs_allowed = models.BooleanField()
	completed_by_semester = models.IntegerField()
	req_lists_inside = models.ManyToManyField('self')
	course_list = models.ManyToManyField("Course")

	def __str__(self):
		return "{0}: max: {1}, min: {2}, double?: {3}, common: {4}, pdfs?: {5}, semester: {6}, inside_req_list: {7}".format(self.name, 
			self.max_counted, self.min_needed, self.double_counting_allowed, self.max_common_with_major, self.pdfs_allowed, self.req_list_inside)

class Concentration(models.Model):
	tipe = models.CharField(max_length=15)
	name = models.CharField(max_length=200)
	code = models.CharField(max_length=3)
	degree = models.CharField(max_length=3)
	year = models.IntegerField()
	urls = models.ManyToManyField(URL)
	contacts = models.ManyToManyField(Contact)

	def __str__(self):
		return "{0}: {1}, {2}, {3}, {4}, {5}, {6}".format(self.name, self.tipe, self.code, self.degree, self.year, self.urls, 
			self.contacts)

class Professor(models.Model):
	uid = models.CharField(max_length=9)
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Listing(models.Model):
	department = models.ForeignKey(Department, on_delete=models.CASCADE)
	number = models.IntegerField()
	x = models.ForeignKey('Course', on_delete=models.CASCADE)

	def __str__(self):
		return self.department

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
		return self.classnum

class Area(models.Model):
	code = models.CharField(max_length=3)
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.code

class Course(models.Model):
	professor = models.ManyToManyField(Professor)
	title = models.CharField(max_length=200)
	courseid = models.IntegerField()
	listings = models.ManyToManyField(Listing)
	area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
	prereqs = models.ManyToManyField('self')
	descrip = models.TextField()

	def __str__(self):
		return self.title



#users
#enrollment
#save templates