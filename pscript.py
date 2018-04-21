from collections import OrderedDict
import json

def timeConverter(time):
	temp = time.split(' ')
	slots = temp[0].split(':')
	if temp[1] == "pm":
		if slots[0][0] == '0':
			hour = str(int(slots[0][1]) + 12)
		else:
			hour = str(int(slots[0]) + 12)
	else:
		hour = slots[0]

	return str(hour + ":" + slots[1] + ":" + slots[2])

outp = ""
outpp = ""
outpl = ""
outpc = ""
outpd = ""
pcounter = 0
lcounter = 0
ccounter = 0
dcounter = 0
pcurr = []
lcurr = []
ccurr = []
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
	outpd += "{{'model':'home.department', 'pk': {0}, 'fields': {{'name': '{1}', 'code': '{2}'}}}}, ".format(dcounter, d, depts[d])
	dcounter += 1

courses = json.load(open("courses.json"))

for i in range(0, len(courses)):
	course = courses[i]
	pcurr.clear()
	lcurr.clear()
	ccurr.clear()

	for p in course["profs"]:
		outpp += """{{'model': 'home.professor', 'pk': {0}, 'fields': {{'uid': '{1}', 'name': '{2}'}}}}, """.format(pcounter, p["uid"], p["name"])
		pcurr.append(pcounter)
		pcounter += 1
	for l in course["listings"]:
		outpl += """{{'model': 'home.listing', 'pk': {0}, 'fields': {{'department': {1}, 'number': {2}}}}}, """.format(lcounter, list(depts.keys()).index(l["dept"]), l["number"])
		lcurr.append(lcounter)
		lcounter += 1
	for c in course["classes"]:
		outpc += """{{'model': 'home.listing', 'pk': {0}, 'fields': {{'classnum': '{1}', 'enroll': {2}, 'limit': {3}, 'starttime': '{4}', 'section': '{5}', 'endtime': '{6}', 'roomnum': {7}, 'days': '{8}', 'bldg': '{9}'}}}}, """.format(lcounter, 
			c["classnum"], c["enroll"], c["limit"], timeConverter(c["starttime"]), c["section"], timeConverter(c["endtime"]), c["roomnum"], c["days"], c["bldg"])
		ccurr.append(ccounter)
		ccounter += 1
	outp += """{{'model': 'home.course', 'pk': {0}, 'fields': {{'title': '{1}', 'courseid': '{2}', 'area': '{3}', 'descrip': '{4}', 'professor': {5}, 'listings': {6}, 'prereqs': [], 'classes': {7}}}}}, """.format(i, 
		course["title"], course["courseid"], course["area"], course["descrip"], pcurr, lcurr, ccurr)

print(outp)

