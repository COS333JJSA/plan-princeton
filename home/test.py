reqs = [{"name": "General Chemistry", "min_needed": 2, "req_lists_inside": [{"name": "Differential and Integral Calculus", "min_needed": 2, "course_list": ["Calculus II", "Calculus I"]}, {"name": "Req2", "min_needed": 4, "course_list": ["c1", "c2"]}]}, {"name": "Gen2", "min_needed": 3, "course_list": ["c3", "c4"]}]

level_one = []
level_two = []
level_three = []
level_four = []
level_five = []
levels = [level_one, level_two, level_three, level_four, level_five]
temp = {}
temp_c = []
temp["titles"] = temp_c
level = 0

for r in reqs:
	temp_c.append(r["name"] + " (" + str(r["min_needed"]) + ")")
	level += 1
	temp2 = {}
	temp2_c = []
	#if another nested level
	#if len(r["req_lists_inside"]) > 0:
	if "req_lists_inside" in r.keys():
		temp2["titles"] = temp2_c
		for r2 in r["req_lists_inside"]:
			temp2_c.append(r2["name"] + " (" + str(r2["min_needed"]) + ")")
			level += 1
			temp3 = {}
			temp3_c = []
			#if another nested level
			#if len(r2["req_lists_inside"]) > 0:
			if "req_lists_inside" in r2.keys():
				temp3["titles"] = temp3_c
				for r3 in r2["req_lists_inside"]:
					temp3_c.append(r3["name"] + " (" + str(r3["min_needed"]) + ")")
					level += 1
					temp4 = {}
					temp4_c = []
					#if another nested level
					#if len(r3["req_lists_inside"]) > 0:
					if "req_lists_inside" in r3.keys():
						temp4["titles"] = temp4_c
						for r4 in r3["req_lists_inside"]:
							temp4_c.append(r4["name"] + " (" + str(r4["min_needed"]) + ")")
							level += 1
							temp5 = {}
							temp5_c = []
							temp5["courses"] = temp5_c
							for c5 in r4.course_list:
								temp5_c.append(c5)
							levels[level].append(temp5)
							level -= 1
					else:
						temp4["courses"] = temp4_c
						for c4 in r3["course_list"]:
							temp4_c.append(c4)
					levels[level].append(temp4)
					level -= 1
			else:
				temp3["courses"] = temp3_c
				for c3 in r2["course_list"]:
					temp3_c.append(c3)
			levels[level].append(temp3)
			level -= 1
	else:
		temp2["courses"] = temp2_c
		for c2 in r["course_list"]:
			temp2_c.append(c2)
	levels[level].append(temp2)
	level -= 1
levels[level].append(temp)

print(levels)






# ret = [[{'titles': ['General Chemistry (2)', 'Gen2 (3)']}], [{'titles': ['Differential and Integral Calculus (2)', 'Req2 (4)']}, {'courses': ['c3', 'c4']}], [{'courses': ['Calculus II', 'Calculus I']}, {'courses': ['c1', 'c2']}], [], []]
ret = levels
icnt = 0
jcnt = 0
kcnt = 0
level = 0


for i in ret[level][0]["titles"]:
	level = 0
	print("h1: " + i)
	level = 1
	if len(ret[level]) > icnt:		
		if "titles" in ret[level][icnt].keys():
			vals = ret[level][icnt]["titles"]
			val = "h2: "
		elif "courses" in ret[level][icnt].keys():
			vals = ret[level][icnt]["courses"]
			val = "obj2: "
		for j in vals:
			level = 1
			print(val + j)
			level = 2
			if len(ret[level]) > jcnt:
				if "titles" in ret[level][jcnt].keys():
					kvals = ret[level][jcnt]["titles"]
					kval = "h3: "
				else:
					kvals = ret[level][jcnt]["courses"]
					kval = "obj3: "
				for k in kvals:
					print(kval + k)
			jcnt += 1
	icnt += 1




# ret = [[['titles', 'General Chemistry (2)', 'Gen2 (3)']], [['titles', 'Differential and Integral Calculus (2)', 'Req2 (4)'], ['courses', 'c3', 'c4']], [['courses', 'Calculus II', 'Calculus I'], ['courses', 'c1', 'c2']], [], []]
# ret = levels
# icnt = 0
# jcnt = 0
# kcnt = 0
# level = 0

# for i in ret[level][0]:
# 	level = 0
# 	print("h1: " + i)
# 	level = 1
# 	if len(ret[level]) > icnt:		
# 		if "titles" in ret[level][icnt].keys():
# 			vals = ret[level][icnt]["titles"]
# 			val = "h2: "
# 		elif "courses" in ret[level][icnt].keys():
# 			vals = ret[level][icnt]["courses"]
# 			val = "obj2: "
# 		for j in vals:
# 			level = 1
# 			print(val + j)
# 			level = 2
# 			if len(ret[level]) > jcnt:
# 				if "titles" in ret[level][jcnt].keys():
# 					kvals = ret[level][jcnt]["titles"]
# 					kval = "h3: "
# 				else:
# 					kvals = ret[level][jcnt]["courses"]
# 					kval = "obj3: "
# 				for k in kvals:
# 					print(kval + k)
# 			jcnt += 1
# 	icnt += 1

