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

# class Req_ListManager(models.Manager):
# 	def get_queryset(self):
# 		return super(ConcentrationManager, self).get_queryset()

# 	def get_concentration(self, conc):
# 		return super(ConcentrationManager, self).get_queryset().get(name = conc)

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
	req_lists_inside = models.ManyToManyField('self', symmetrical=False, blank=True)
	course_list = models.ManyToManyField("Course", blank=True)
	# objects = Req_ListManager()

	def __str__(self):
		return str(self.name)

class ConcentrationManager(models.Manager):
	def get_queryset(self):
		return super(ConcentrationManager, self).get_queryset()
	# def get_reqs(self, conc):
	# 	level_one = []
	# 	level_two = []
	# 	level_three = []
	# 	level_four = []
	# 	level_five = []
	# 	levels = [level_one, level_two, level_three, level_four, level_five]
	# 	temp = {}
	# 	temp_c = []
	# 	temp["titles"] = temp_c
	# 	level = 0
	# 	return 

		# for r in reqs:
		# 	temp_c.append(r.name + " (" + str(r.min_needed) + ")")
		# 	level += 1
		# 	temp2 = {}
		# 	temp2_c = []
		# 	#if another nested level
		# 	#if len(r["req_lists_inside"]) > 0:
		# 	if "req_lists_inside" in r.keys():
		# 		temp2["titles"] = temp2_c
		# 		for r2 in r["req_lists_inside"]:
		# 			temp2_c.append(r2["name"] + " (" + str(r2["min_needed"]) + ")")
		# 			level += 1
		# 			temp3 = {}
		# 			temp3_c = []
		# 			#if another nested level
		# 			#if len(r2["req_lists_inside"]) > 0:
		# 			if "req_lists_inside" in r2.keys():
		# 				temp3["titles"] = temp3_c
		# 				for r3 in r2["req_lists_inside"]:
		# 					temp3_c.append(r3["name"] + " (" + str(r3["min_needed"]) + ")")
		# 					level += 1
		# 					temp4 = {}
		# 					temp4_c = []
		# 					#if another nested level
		# 					#if len(r3["req_lists_inside"]) > 0:
		# 					if "req_lists_inside" in r3.keys():
		# 						temp4["titles"] = temp4_c
		# 						for r4 in r3["req_lists_inside"]:
		# 							temp4_c.append(r4["name"] + " (" + str(r4["min_needed"]) + ")")
		# 							level += 1
		# 							temp5 = {}
		# 							temp5_c = []
		# 							temp5["courses"] = temp5_c
		# 							for c5 in r4.course_list:
		# 								temp5_c.append(c5)
		# 							levels[level].append(temp5)
		# 							level -= 1
		# 					else:
		# 						temp4["courses"] = temp4_c
		# 						for c4 in r3["course_list"]:
		# 							temp4_c.append(c4)
		# 					levels[level].append(temp4)
		# 					level -= 1
		# 			else:
		# 				temp3["courses"] = temp3_c
		# 				for c3 in r2["course_list"]:
		# 					temp3_c.append(c3)
		# 			levels[level].append(temp3)
		# 			level -= 1
		# 	else:
		# 		temp2["courses"] = temp2_c
		# 		for c2 in r["course_list"]:
		# 			temp2_c.append(c2)
		# 	levels[level].append(temp2)
		# 	level -= 1
		# levels[level].append(temp)




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
	#  super(ConcentrationManager, self).get_queryset()
	#objects = ConcentrationManager()
	# sample_plans = models.ManyToManyField('Plan')

	def __str__(self):
		return str(self.name)

	def get_description(self):
		return self.req_lists

	def get_reqs(self):
		temp = []
		for r in self.req_lists.all():
			temp.append(r.name + " (" + str(r.min_needed) + ")")
			temp2 = []
			print("here1")
			print(len(r.req_lists_inside.all()))
			print(r.req_lists_inside.all())
			if len(r.req_lists_inside.all()):
				for r2 in r.req_lists_inside.all():
					temp2.append(r2.name + " (" + str(r2.min_needed) + ")")
					temp3 = []
					print("here2")
					print(len(r2.req_lists_inside.all()))
					print(r2.req_lists_inside.all())
					if len(r2.req_lists_inside.all()):
						for r3 in r2.req_lists_inside.all():
							temp3.append(r3.name + " (" + str(r3.min_needed) + ")")
							temp4 = []
							if len(r3.req_lists_inside.all()):
								for r4 in r3.req_lists_inside.all():
									temp2.append(r4.name + " (" + str(r4.min_needed) + ")")
							else:
								for c4 in r3.course_list.all():
									temp2.append(c4)
						temp3.append(temp4)
					else:
						for c3 in r2.course_list.all():
							temp2.append(c3)
				temp2.append(temp3)
			else:
				for c2 in r.course_list.all():
					temp2.append(c2)
		temp.append(temp2)
		return temp

	# def get_reqs(self):
	# 	# reqs = [{"name": "General Chemistry", "min_needed": 2, "req_lists_inside": [{"name": "Differential and Integral Calculus", "min_needed": 2, "course_list": ["Calculus II", "Calculus I"]}, {"name": "Req2", "min_needed": 4, "course_list": ["c1", "c2"]}]}, {"name": "Gen2", "min_needed": 3, "course_list": ["c3", "c4"]}]
	# 	# reqs = 
	# 	level_one = []
	# 	level_two = []
	# 	level_three = []
	# 	level_four = []
	# 	level_five = []
	# 	levels = [level_one, level_two, level_three, level_four, level_five]
	# 	temp = {}
	# 	temp_c = []
	# 	temp["titles"] = temp_c
	# 	level = 0

	# 	for r in reqs:
	# 		temp_c.append(r.name + " (" + str(r.min_needed) + ")")
	# 		level += 1
	# 		temp2 = {}
	# 		temp2_c = []
	# 		#if another nested level
	# 		#if len(r["req_lists_inside"]) > 0:
	# 		if "req_lists_inside" in r.keys():
	# 			temp2["titles"] = temp2_c
	# 			for r2 in r.req_lists_inside:
	# 				temp2_c.append(r2.name + " (" + str(r2.min_needed) + ")")
	# 				level += 1
	# 				temp3 = {}
	# 				temp3_c = []
	# 				#if another nested level
	# 				#if len(r2["req_lists_inside"]) > 0:
	# 				if "req_lists_inside" in r2.keys():
	# 					temp3["titles"] = temp3_c
	# 					for r3 in r2.req_lists_inside:
	# 						temp3_c.append(r3.name + " (" + str(r3.min_needed) + ")")
	# 						level += 1
	# 						temp4 = {}
	# 						temp4_c = []
	# 						#if another nested level
	# 						#if len(r3["req_lists_inside"]) > 0:
	# 						if "req_lists_inside" in r3.keys():
	# 							temp4["titles"] = temp4_c
	# 							for r4 in r3.req_lists_inside:
	# 								temp4_c.append(r4.name + " (" + str(r4.min_needed) + ")")
	# 								level += 1
	# 								temp5 = {}
	# 								temp5_c = []
	# 								temp5["courses"] = temp5_c
	# 								for c5 in r4.course_list:
	# 									temp5_c.append(c5)
	# 								levels[level].append(temp5)
	# 								level -= 1
	# 						else:
	# 							temp4["courses"] = temp4_c
	# 							for c4 in r3.course_list:
	# 								temp4_c.append(c4)
	# 						levels[level].append(temp4)
	# 						level -= 1
	# 				else:
	# 					temp3["courses"] = temp3_c
	# 					for c3 in r2.course_list:
	# 						temp3_c.append(c3)
	# 				levels[level].append(temp3)
	# 				level -= 1
	# 		else:
	# 			temp2["courses"] = temp2_c
	# 			for c2 in r.course_list:
	# 				temp2_c.append(c2)
	# 		levels[level].append(temp2)
	# 		level -= 1
	# 	levels[level].append(temp)

	# 	return levels

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
	def all_info(self):
		dic = {}
		all_courses = Course.objects.all()
		for c in all_courses:
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
	objects = CourseManager()

	def title_and_code(self):
		st = ""
		for l in self.listings.all():
			st += str(l.department.code) + " " + str(l.number)
			st += "/"
		st = st[:len(st)-1]
		st += ": " + self.title
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
	plans = models.ManyToManyField('Plan')

	objects = UserManager()

class Plan(models.Model):
 	saved_courses = models.ManyToManyField('SavedCourse')

class SavedCourse(models.Model):
	course = models.ManyToManyField('Course')
	semester = models.ManyToManyField('Semester')

class Semester(models.Model):
	season = models.CharField(max_length=1)
	year = models.IntegerField()