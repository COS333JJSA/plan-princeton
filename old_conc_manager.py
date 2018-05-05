
# 	def get_BSE(self, conc):
# 		reqs = {}
# 		for req in super(ConcentrationManager, self).get_queryset().get(name=conc).req_lists.get(name='Prerequisites').req_lists_inside.all():
# 			courses = []
# 			courses.append(req.min_needed)
# 			for course in req.course_list.all():
# 				courses.append(course.title)
# 			reqs[req.name] = courses
# 			#print (req)
# 			#for c in req.:
# 				#print (course)
# 				#print subreq.course_list
# 		return reqs

# class ConcentrationManager(models.Manager):

# 	def get_BSE(self, conc):
# 		reqs = []
# 		for req in super(ConcentrationManager, self).get_queryset().get(name=conc).req_lists.get(name='Prerequisites').req_lists_inside.all():
# 			courses = []
# 			courses.append(req.min_needed)
# 			for course in req.course_list.all():
# 				courses.append(course.title)
# 			reqs.append(req.name)
# 			reqs.append(req.min_needed)
# 			reqs.append(courses)
# 		return reqs


# for r in reqs:
# 	level_one.append(r.name)
# 	if len(r.req_lists_inside) > 0:
# 		for r2 in r.req_lists_inside:
# 			level_two.append(r2.name)
# 			if len(r2.req_lists_inside) > 0:
# 				for r3 in r2.req_lists_inside:
# 					level_three.append(r3.name)
# 			else:
# 				for c3 in r2.course_list:
# 					level_three.append(c3.title)
