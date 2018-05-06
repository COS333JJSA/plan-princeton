from collections import OrderedDict
import json
import sys
import re

def timeConverter(time):
	temp = time.split(" ")
	slots = temp[0].split(":")
	if temp[1] == "pm":
		if slots[0] == "12":
			hour = str(slots[0])
		elif slots[0][0] == "0":
			hour = str(int(slots[0][1]) + 12)
		else:
			hour = str(int(slots[0]) + 12)
	else:
		hour = slots[0]

	return str(hour + ":" + slots[1] + ":" + slots[2])

def stringify(listing):
	return(listing["dept"] + " " + listing["number"])

def escape(s):
	char = []
	if s == None:
		return ""
	for c in s:
		if c == '"':
			char.append('\\')
			char.append('"')
		else:
			char.append(c)
	return ''.join(char)

def req_recursion(req, myid, parentid):
	global r
	global req_lists
	req["myid"] = myid
	req["parentid"] = parentid
	req_lists.append(req)

	if "req_list" in req.keys():
		for reg in req["req_list"]:
			r += 1
			req_recursion(reg, r, myid)

	curr = []
	for reg in req_lists:
		if reg["parentid"] == myid:
			curr.append(reg["myid"])

	make_req_list(req, myid, curr)

#for courses with *s, load all qualifying courses into c_pks
def starcourses(c, c_pks):
	if c[4] != '*':
		send = c[0:5] + ".*"
	else:
		send = c[0:4] + ".*"
	for course in course_pks:
		if re.search(send, course) != None:
			c_pks.append(course_pks[course])
	return c_pks

#create req_list object from information in req
def make_req_list(req, myid, curr):
	global outp
	c_pks = []
	#course list
	if "course_list" in req.keys():
		for c in req["course_list"]:
			if '*' in c:
				starcourses(c, c_pks)
			else:
				c_pks.append(course_pks[c[0:7]])
	#description
	if "description" not in req.keys():
		req["description"] = ""
	#explanation
	if "explanation" not in req.keys():
		req["explanation"] = ""
	#double_counting_allowed default false
	if "double_counting_allowed" not in req.keys():
		req["double_counting_allowed"] = "false"
	elif req["double_counting_allowed"] == "True" or req["double_counting_allowed"] == "true":
		req["double_counting_allowed"] = "true"
	else:
		req["double_counting_allowed"] = "false"
	#max common
	if "max_common_with_major" not in req.keys():
		req["max_common_with_major"] = "null"
	elif req["max_common_with_major"] == "":
		req["max_common_with_major"] = "null"
	#pdfs allowed
	if "pdfs_allowed" not in req.keys():
		req["pdfs_allowed"] = "null"
	elif req["pdfs_allowed"] == "":
		req["pdfs_allowed"] = "null"
	#completed_by_semester
	if "completed_by_semester" not in req.keys():
		req["completed_by_semester"] = 8

	outp += """{{"model": "home.req_list", "pk": {0}, "fields": {{"name": "{1}", "max_counted": {2}, "min_needed": {3}, "description": "{4}", "explanation": "{5}", "double_counting_allowed": {6}, "max_common_with_major": {7}, "pdfs_allowed": {8}, "completed_by_semester": {9}, "req_lists_inside": {10}, "course_list": {11}}}}}, """.format(
		myid, req["name"], req["max_counted"], req["min_needed"], escape(req["description"]), escape(req["explanation"]), req["double_counting_allowed"], req["max_common_with_major"], req["pdfs_allowed"], req["completed_by_semester"], curr, c_pks)


outp = ""
pcounter = 0
lcounter = 0
ccounter = 0
dcounter = 0
acounter = 0
scounter = 0
pcurr = []
lcurr = []
ccurr = []
scurr = []
course_pks = {}
areas = OrderedDict({"EC": "Epistemology and Cognition", "EM": "Ethical Thought and Moral Values", "HA": "Historical Analysis", "LA": 
	"Literature and the Arts", "SA": "Social Analysis", "QR": "Quantitative Reasoning", "STN": "Science and Technology - no lab",
	"STL": "Science and Technology = lab"})
depts = OrderedDict({"AAS": "African American Studies", "ANT": "Anthropology", "ARC": "Architecture", "ART": "Art and Archaeology",
	"AST": "Astrophysical Sciences", "CHM": "Chemistry", "CLA": "Classics", "COM": "Comparative Literature",
	"COS": "Computer Science", "EAS": "East Asian Studies", "EEB": "Ecology and Evolutionary Biology", "ECO": "Economics",
	"ENG": "English", "FRE": "French and Italian", "GEO": "Geosciences", "GER": "German", "HIS": "History", "MAT": "Mathematics",
	"MOL": "Molecular Biology", "MUS": "Music", "NES": "Near Eastern Studies", "NEU": "Neuroscience", "PHI": "Philosophy",
	"PHY": "Physics", "POL": "Politics", "PSY": "Psychology", "REL": "Religion", "SLA": "Slavic Languages and Literature",
	"SOC": "Sociology", "SPA": "Spanish", "WWS": "Woodrow Wilson School of Public and International Affairs",
	"CBE": "Chemical and Biological Engineering", "CEE": "Civil and Environmental Engineering", "ELE": "Electrical Engineering",
	"MAE": "Mechanical and Aerospace Engineering", "ORF": "Operations Research and Financial Engineering", 
	"COS-AB": "AB Computer Science", "COS-BSE": "BSE Computer Science", "GSS": "Gender and Sexuality Studies", "LAS": 
	"Latin American Studies", "AFS": "African Studies", "AMS": "American Studies", "AOS":"Atmospheric & Oceanic Studies",
	"PAC": "Applications of Computing", "APC": "Applied and Computational Mathematics", "ASA": "Asian American Studies",
	"ATL": "Atelier", "BCS": "Bosnian-Coatian-Serbian", "CHI": "Chinese", "CHV": "Center for Human Values", "CLG": "Classical Greek",
	"CTL": "Center for Teaching & Learning", "CWR": "Creative Writing", "CZE": "Czech", "DAN": "Dance", "ECS": "European Cultural Studies",
	"EGR": "Engineering", "ENE": "Energy Studies", "ENT": "Entrepreneurship", "ENV": "Environmental Studies", "EPS": 
	"Contemporary European Politics", "FIN": "Finance", "FRS": "Freshman Seminars", "GHP": "Global Health and Health Policy", 
	"GLS": "Global Seminar", "HEB": "Hebrew", "HIN": "Hindi", "HLS": "Hellenic Studies", "HOS": "History of Science",
	"HPD": "History/Practice of Diplomacy", "HUM": "Humanistic Studies", "ISC": "Integrated Science Curriculum", "ITA": "Italian",
	"JDS": "Judaic Studies", "JPN": "Jananese", "JRN": "Journalism", "KOR": "Korean", "LAO": "Latino Studies", "LAT": "Latin",
	"LCA": "Lewis Center for the Arts", "LIN": "Linguistics", "MED": "Mideval Studies", "MOD": "Media and Modernity", "MOG": 
	"Modern Greek", "MSE": "Materials Science and Engineering", "MTD": "Music Theater", "PAW": "Ancient World", "PER": "Persian",
	"PLS": "Polish", "POP": "Population Studies", "POR": "Portuguese", "PSY": "Psychology", "QCB": "Quantitative Computational Biology",
	"RES": "Russian, East European, and Eurasian Studies", "SAN": "Sanskrit", "SAS": "South Asian Studies", "SML": 
	"Statistics and Machine Learning", "STC": "Science and Technology Council", "SWA": "Swahili", "THR": "Theater",
	"TPP": "Teacher Preparation", "TRA": "Translation and Intercultural Communication", "TUR": "Turkish", "TWI": "Twi",
	"URB": "Urban Studies", "URD": "Urdu", "VIS": "Visual Arts", "WRI": "Princeton Writing Program", "ARA": "Arabic",
	"CGS": "Cognitive Science", "SPO": "Spanish and Portuguese", "RUS": "Russian"
	})

for d in depts:
	outp += """{{"model":"home.department", "pk": {0}, "fields": {{"name": "{2}", "code": "{1}"}}}}, """.format(dcounter, d, depts[d])
	dcounter += 1

for a in areas:
	outp += """{{"model": "home.area", "pk": {0}, "fields": {{"code": "{1}", "name": "{2}"}}}}, """.format(acounter, a, areas[a])
	acounter += 1

courses = json.load(open("courses.json"))

#serialize courses
for i in range(0, len(courses)):
	course = courses[i]
	for l in course["listings"]:
		course_pks[stringify(l)] = i

#make course objects
for i in range(0, len(courses)):
	course = courses[i]
	pcurr.clear()
	lcurr.clear()
	ccurr.clear()
	scurr.clear()

	for p in course["profs"]:
		outp += """{{"model": "home.professor", "pk": {0}, "fields": {{"uid": "{1}", "name": "{2}"}}}}, """.format(pcounter, p["uid"], p["name"])
		pcurr.append(pcounter)
		pcounter += 1
	for l in course["listings"]:
		outp += """{{"model": "home.listing", "pk": {0}, "fields": {{"department": {1}, "number": {2}}}}}, """.format(lcounter, list(depts.keys()).index(l["dept"]), l["number"])
		lcurr.append(lcounter)
		lcounter += 1
	for c in course["classes"]:
		outp += """{{"model": "home.class", "pk": {0}, "fields": {{"classnum": "{1}", "enroll": {2}, "limit": {3}, "starttime": "{4}", "section": "{5}", "endtime": "{6}", "roomnum": "{7}", "days": "{8}", "bldg": "{9}"}}}}, """.format(ccounter, 
			c["classnum"], c["enroll"], c["limit"], timeConverter(c["starttime"]), c["section"], timeConverter(c["endtime"]), c["roomnum"], c["days"], c["bldg"])
		ccurr.append(ccounter)
		ccounter += 1
	for s in course["term"]:
		s = s.split()
		outp += """{{"model": home.semester", "pk": {0}, "fields": {{"season": "{1}", "year": {2}}}}}, """.format(scounter, s[0], s[1])
		scurr.append(scounter)
		scounter += 1
	#check for area
	if course["area"] == "":
		area = "null"
	else:
		area = list(areas.keys()).index(course["area"])
	outp += """{{"model": "home.course", "pk": {0}, "fields": {{"title": "{1}", "courseid": "{2}", "area": {3}, "descrip": "{4}", "professor": {5}, "listings": {6}, "prereqs": [], "classes": {7}}}}}, """.format(i, 
		escape(course["title"]), course["courseid"], area, escape(course["descrip"]), pcurr, lcurr, ccurr)


concs = json.load(open("reqs_abbrv"))
r = 0
ucounter = 0
ccounter = 0
req_lists = []
rcurr = []
ucurr = []
ccurr = []

for k in range(0, len(concs)):
	conc = concs[k]
	rcurr.clear()
	ucurr.clear()
	ccurr.clear()
	#preprocess req_lists
	for reg in conc["req_list"]:
		r += 1
		rcurr.append(r)
		req_recursion(reg, r, 0)
		

	#add urls
	for u in conc["urls"]:
		outp += """{{"model": "home.url", "pk": {0}, "fields": {{"url": "{1}"}}}}, """.format(ucounter, u)
		ucurr.append(ucounter)
		ucounter += 1
	#add contacts
	for c in conc["contacts"]:
		outp += """{{"model": "home.contact", "pk": {0}, "fields": {{"tipe": "{1}", "name": "{2}", "email": "{3}"}}}}, """.format(ccounter, c["type"], c["name"], c["email"])
		ccurr.append(ccounter)
		ccounter += 1

	if "degree" not in conc.keys():
		conc["degree"] = "AB"
	#add req
	outp += """{{"model": "home.concentration", "pk": {0}, "fields": {{"tipe": "{1}", "name": "{2}", "conc_code": {3}, "degree": "{4}", "year": {5}, "urls": {6}, "contacts": {7}, "req_lists": {8}}}}}, """.format(k, conc["type"], conc["name"], list(depts.keys()).index(conc["code"]), conc["degree"], conc["year"], ucurr, ccurr, rcurr)


print("[" + outp[:len(outp) - 2] + "]")


