
#course_pks: dict key: COS 126 value: pk
sems = {"spring 2018": 0, "fall 2018": 1}

saved_course_counter = 0

for i in file_plans:
	fall1 = i["Freshman Fall"]
	fall2 = i[""]

	#key: COS 126 value: pk
	saved_course_pks = []
	sems = [fall1, fall2, spring1, spring2]
	for sem in sems:
		for c in sem:
			course_pk = course_pks[c]
			sem_pk = 1
			outp += """{{"model": "home.SavedCourse", "pk": {0}, "fields": {{"course": "{1}", "semester": "{2}"}}}}, """.format(i, )
			saved_course_pks.append(saved_course_counter)
			saved_course_counter += 1

	for 



	outp += """{{"model": "home.plan", "pk": {0}, "fields": {{"degree": "{1}", "conc": "{2}", "saved_courses": {3}}}, """.format(i, 
		escape(course["title"]), course["courseid"], area, escape(course["descrip"]), pcurr, lcurr, ccurr, scurr, course["term"][0][0])
