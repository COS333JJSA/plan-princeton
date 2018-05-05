reqs = [{"name": "General Chemistry", "min_needed": 2, "req_lists_inside": [{"name": "Differential and Integral Calculus", "min_needed": 2, "course_list": ["Calculus II", "Calculus I"]}, {"name": "Req2", "min_needed": 4, "course_list": ["c1", "c2"]}]}, {"name": "Gen2", "min_needed": 3, "course_list": ["c3", "c4"]}]

temp = []
for r in self.req_lists.all():
	temp.append(r.name + " (" + str(r.min_needed) + ")")
	temp2 = []
	if r.req_lists_inside:
		for r2 in r.req_lists_inside.all():
			temp2.append(r2.name + " (" + str(r2.min_needed) + ")")
			temp3 = []
			if r2.req_lists_inside:
				for r3 in r2.req_lists_inside.all():
					temp3.append(r3.name + " (" + str(r3.min_needed) + ")")
					temp4 = []
					if r3.req_lists_inside:
						for r4 in r3.req_lists_inside.all():
							temp2.append(r4.name + " (" + str(r4.min_needed) + ")")
					else:
						for c4 in reqs.course_list.all():
							temp2.append(c4)
				temp3.append(temp4)
			else:
				for c3 in reqs.course_list.all():
					temp2.append(c3)
		temp2.append(temp3)
	else:
		for c2 in reqs.course_list.all():
			temp2.append(c2)
temp.append(temp2)
print(temp)



