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

class Req_List(models.Model):
	name = models.CharField(max_length=100)
	max_counted = models.IntegerField(default=1)
	min_needed = models.IntegerField(default=0)
	description = models.CharField(max_length=400, blank=True, null=True)
	explanation = models.TextField(blank=True, null=True)
	double_counting_allowed = models.BooleanField(default=False)
	max_common_with_major = models.IntegerField(null=True, blank=True)
	pdfs_allowed = models.IntegerField(null=True, blank=True)
	completed_by_semester = models.IntegerField(default=8)
	req_lists_inside = models.ManyToManyField('self', symmetrical=False, blank=True)
	course_list = models.ManyToManyField("Course", blank=True)

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
	# sample_plans = models.ManyToManyField('Plan')

	def __str__(self):
		return str(self.name)

	def code_and_name(self):
		return self.conc_code.code + " (" + self.name + ")"

	def get_description(self):
		return self.req_lists

	def get_reqs(self):
		r_array = self.req_lists.all()
		temp = []
		for r in r_array:
			temp.append(r.name + " (" + str(r.min_needed) + ")")
			temp2 = []
			if len(r.req_lists_inside.all()):
				for r2 in r.req_lists_inside.all():
					temp2.append(r2.name + " (" + str(r2.min_needed) + ")")
					temp3 = []
					if len(r2.req_lists_inside.all()):
						for r3 in r2.req_lists_inside.all():
							temp3.append(r3.name + " (" + str(r3.min_needed) + ")")
							temp4 = []
							if len(r3.req_lists_inside.all()):
								for r4 in r3.req_lists_inside.all():
									temp2.append(r4.name + " (" + str(r4.min_needed) + ")")
							else:
								for c4 in r3.course_list.all():
									temp4.append(c4.codes())
							temp3.append(temp4)
					else:
						for c3 in r2.course_list.all():
							temp3.append(c3.codes())
					temp2.append(temp3)
			else:
				for c2 in r.course_list.all():
					temp2.append(c2.codes())
			temp.append(temp2)
		return temp


	def update_reqs(self, courses):
		new_courses = []
		for i in courses:
			new_courses.append(Course.objects.get(courseid=i.courseid).title_and_code())
		return self.reqing(new_courses, self.get_reqs())

		

	def reqing(self, courses, arr):
		new_courses = courses

		# def calculator()
		for c0 in range(0, len(arr)):
			r = arr[c0]
			if type(r) == list:
				for c1 in range(0, len(r)):
					r2 = r[c1]
					if type(r2) == list:
						for c2 in range(0, len(r2)):
							r3 = r2[c2]
							if type(r3) == list:
								for c3 in range(0, len(r3)):
									r4 = r3[c3]
									if r4 in new_courses:
										r3.remove(r4)
										if len(r3) == 0:
											r2.remove(r3)
										temp4 = int(r2[c2-1][len(r2[c2-1])-2]) - 1
										if temp4 == 0:
											r2.remove(r2[c2-1])
										else:
											r2[c2-1] = str(r2[c2-1][0:len(r2[c2-1])-2] + str(temp4) + ")")
										if len(r2) == 0:											
											r.remove(r2)
										temp4a = int(r[c1-1][len(r[c1-1])-2]) - 1
										if temp4a == 0:
											r.remove(r[c1-1])
										else:
											r[c1-1] = str(r[c1-1][0:len(r[c1-1])-2] + str(temp4a) + ")")
										if len(r) == 0:
											arr.remove(r)
										temp4b = int(arr[c0-1][len(arr[c0-1])-2]) - 1
										if temp4b == 0:
											return arr.remove(arr[c0-1])
										else:
											arr[c0-1] = str(arr[c0-1][0:len(arr[c0-1])-2] + str(temp4b) + ")")
										return self.reqing(new_courses, arr)
							elif r3 in new_courses:
								r2.remove(r3)
								if len(r2) == 0:
									r.remove(r2)
								temp3 = int(r[c1-1][len(r[c1-1])-2]) - 1
								if temp3 == 0:
									r.remove(r[c1-1])
								else:
									r[c1-1] = str(r[c1-1][0:len(r[c1-1])-2] + str(temp3) + ")")
								if len(r) == 0:
									arr.remove(r)
								temp3a = int(arr[c0-1][len(arr[c0-1])-2]) - 1
								if temp3a == 0:
									arr.remove(arr[c0-1])
								else:
									arr[c0-1] = str(arr[c0-1][0:len(arr[c0-1])-2] + str(temp3a) + ")")
								return self.reqing(new_courses, arr)

					elif r2 in new_courses:
						r.remove(r2)
						if len(r) == 0:
							return None
						temp2 = int(arr[c0-1][0:len(arr[c0-1])-2]) - 1
						if temp2 == 0:
							arr.remove(arr[c0-1])
						else:
							arr[c0-1] = str(arr[c0-1][len(arr[c0-1])-2] + str(temp2) + ")")
						return self.reqing(new_courses, arr)
		return arr


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

class CourseManager(models.Manager):
	# takes all courses and creates one dict where keys are course ids and values are information
	def all_info(self):
		dic = {}
		all_courses = Course.objects.all()
		for c in all_courses:
			dic.update(c.all_info_solo())
		return dic
	# list of courses
	def all_info_some(self, courses):
		dic = {}
		for c in courses:
			dic.update(c.all_info_solo())
		return dic

class Course(models.Model):
	professor = models.ManyToManyField(Professor)
	title = models.CharField(max_length=200)
	courseid = models.CharField(max_length=8)
	listings = models.ManyToManyField(Listing)
	area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True)
	prereqs = models.ManyToManyField('self', blank=True)
	classes = models.ManyToManyField('Class')
	descrip = models.TextField()
	semesters = models.ManyToManyField('Semester')
	season = models.TextField()
	objects = CourseManager()

	def title_and_code(self):
		st = ""
		for l in self.listings.all():
			st += str(l.department.code) + " " + str(l.number)
			st += "/"
		st = st[:len(st)-1]
		st += ": " + self.title
		return st
	def codes(self):
		st = ""
		for l in self.listings.all():
			st += str(l.department.code) + " " + str(l.number)
			st += "/"
		st = st[:len(st)-1]
		return st

	def all_info_solo(self):
		d = {}
		s = []
		for p in self.professor.all():
			s.append(p.name)
		d[self.courseid] = {"coursename": self.title_and_code(), "title": self.title, "professors": s, "description": self.descrip}
		return d

	def __str__(self):
		return str(self.title)

class UserManager(models.Manager):
	def create_user(self, ni):
		user = self.create(netid=ni)
		return user
		
class User(models.Model):
	netid = models.CharField(max_length = 100)
	plan = models.ForeignKey('Plan', on_delete=models.SET_NULL, null=True, blank=True)
	objects = UserManager()

class Plan(models.Model):
	degree = models.CharField(max_length=3, null=True, blank=True)
	conc = models.ForeignKey(Concentration, on_delete=models.SET_NULL, null=True, blank=True)
	saved_courses = models.ManyToManyField('SavedCourse', blank=True)

	def return_by_sem(self):
		fall18 = []
		fall19 = []
		spring19 = []
		spring20 = []
		planbysem = {}
<<<<<<< HEAD
		for c in Course.objects.all():
			for code in c.codes():
				if code == "FRS 109" or code == "ISC 231" or code == "ISC 232" or code == "WRI 190":
					fall18.append(c)
				if code == "CHM 302b" or code == "MAT 201" or code == "CWR 201" or code == "HUM 302" or code =="PHI 203":
					fall19.append(c)
				if code == "ISC 233" or code == "ISC 234" or code == "FRS 169" or code == "FRE 107":
					spring19.append(c)
				if code == "CHM 302b" or code == "MAT 201" or code == "CWR 201" or code == "HUM 302" or code == "PHI 203":
					spring20.append(course)
=======
		for course in self.saved_courses.all():
			if course.semester.year == 18 and course.semester.season == 'f':
				fall18.append(course.course)
			if course.semester.year == 19 and course.semester.season == 'f':
				fall19.append(course.course)
			if course.semester.year == 19 and course.semester.season == 's':
				spring19.append(course.course)
			if course.semester.year == 20 and course.semester.season == 's':
				spring20.append(course.course)
>>>>>>> 368697da5935521235b5b808841164485ee14578
		planbysem = {'fall18': Course.objects.all_info_some(fall18), 'fall19': Course.objects.all_info_some(fall19), 'spring19': Course.objects.all_info_some(spring19), 'spring20': Course.objects.all_info_some(spring20)}
		return planbysem
	def return_courses(self):
		courses = []
		for s_course in self.saved_courses.all():
			courses.append(s_course.course)
		return courses

class SavedCourse(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
	semester = models.ForeignKey('Semester', on_delete=models.CASCADE, null=True, blank=True)

class Semester(models.Model):
	season = models.CharField(max_length=1)
	year = models.IntegerField()
