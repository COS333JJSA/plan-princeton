from collections import OrderedDict
import json
import sys
import re

#HELPER FUNCTIONS
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
	c = []
	if s == None or len(s) == 0:
		return ""
	elif s.find('&#39;') != -1:
		c.append(s[0:s.find('&#39;')])
		c.append('\'')
		c.append(s[(s.find('&#39;')+5):])
	elif s.find('&amp') != -1:
		c.append(s[0:s.find('&amp;')])
		c.append('&')
		c.append(s[(s.find('&amp;')+5):])
	elif s[0] == '"':
		c.append('\\')
		c.append(s)
	elif re.search(r"[A-Za-z\s\.,\?!\(\)]\"", s) != None:
		st = re.search(r"[A-Za-z\s\.,\?!\(\)]\"", s).end()
		c.append(s[0:st-1])
		c.append('\\"')
		c.append(s[(st):])
	else:
		for char in s:
			c.append(char)
		return(''.join(c))
	return(escape(''.join(c)))

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
	if c[0:4] == "LANG":
		langs = ["ARA","BCS","SLA","CHI","CZE","FRE","GER","MOG","CLG","HEB","HIN","ITA","JPN","KOR","LAT","PER","PLS","POR","RUS","SPA","SWA","TUR","TWI","URD"]
		# LANG XXX
		if '*' not in c:
			for l in langs:
				send = l + " " + c[5:len(c)]
				for course in course_pks:
					if re.search(send, course) != None:
						c_pks.append(course_pks[course])
		# LANG 2**
		elif c[4] != '*':
			for l in langs:
				send = l + " " + c[5] + ".*"
				for course in course_pks:
					if re.search(send, course) != None:
						c_pks.append(course_pks[course])
		#LANG *
		else:
			send = c[0:4] + ".*"
			for course in course_pks:
				if course[0:3] in langs:
					c_pks.append(course_pks[course])
	else:
		if c[4] != '*':
			send = c[0:5] + ".*"
		else:
			send = c[0:4] + ".*"
		for course in course_pks:
			if re.search(send, course) != None:
				c_pks.append(course_pks[course])
	return c_pks


#REQ_LISTS
#create req_list object from information in req
def make_req_list(req, myid, curr):
	global outp
	c_pks = []
	#course list
	if "course_list" in req.keys():
		for c in req["course_list"]:
			if '*' in c or 'LANG' in c:
				starcourses(c, c_pks)
			else:
				c_pks.append(course_pks[c[0:7]])
	if "dist_req" in req.keys():
		c_pks = area_info[req["dist_req"]]
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


#STATIC INFO and DECLARATIONS
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
	"ENG": "English", "FRE": "French", "GEO": "Geosciences", "GER": "German", "HIS": "History", "MAT": "Mathematics",
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
	"CGS": "Cognitive Science", "SPO": "Spanish and Portuguese", "RUS": "Russian", "FIT": "French and Italian", "AB": "Bachelor of Arts Degree",
	"BSE": "Bachelor of Science and Engineering Degree"
	})

area_info = {"EM": [803, 114, 198, 202, 203, 268, 416, 428, 495, 550, 551, 714, 716, 758, 762, 768, 769, 802, 814, 815, 850, 860, 862, 863, 1000, 1052, 1053, 1210, 1211, 1213, 1214, 1218, 1231, 1290, 1291, 1319, 1410, 1420, 1447, 1457, 1459, 1472, 1512, 1568, 1717, 1763, 1767, 1787, 1788, 1790, 1838, 1840, 1842, 1874, 1875, 1876, 1925], "SA": [3, 277, 816, 967, 0, 8, 14, 17, 19, 20, 21, 22, 23, 25, 26, 29, 31, 99, 261, 263, 267, 278, 279, 280, 282, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 295, 296, 297, 298, 433, 434, 450, 493, 494, 576, 577, 578, 579, 587, 588, 589, 601, 707, 709, 710, 799, 800, 801, 804, 805, 806, 807, 810, 811, 812, 813, 817, 818, 819, 848, 903, 904, 906, 907, 955, 959, 969, 993, 994, 995, 996, 998, 999, 1001, 1002, 1029, 1031, 1034, 1040, 1043, 1044, 1046, 1049, 1054, 1055, 1057, 1058, 1059, 1060, 1081, 1082, 1085, 1086, 1212, 1232, 1282, 1293, 1307, 1308, 1310, 1311, 1312, 1313, 1314, 1315, 1316, 1318, 1321, 1323, 1345, 1358, 1418, 1427, 1430, 1444, 1460, 1477, 1461, 1466, 1471, 1474, 1479, 1480, 1484, 1511, 1514, 1594, 1601, 1602, 1616, 1711, 1718, 1791, 1789, 1792, 1795, 1796, 1797, 1798, 1799, 1800, 1801, 1802, 1803, 1834, 1843, 1846, 1849, 1870, 1882, 1884, 1885, 1886, 1887, 1888, 1890, 1891, 1936, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2025, 2027, 2028, 2029, 2031, 2032, 1464, 1465, 1883], "EC": [13, 24, 30, 149, 150, 184, 429, 487, 553, 596, 597, 598, 600, 602, 603, 604, 715, 757, 759, 760, 761, 763, 764, 765, 766, 767, 843, 846, 847, 866, 997, 1042, 1050, 1051, 1056, 1108, 1112, 1116, 1182, 1292, 1359, 1456, 1462, 1476, 1502, 1503, 1504, 1567, 1612, 1613, 1614, 1615, 1617, 1618, 1729, 1760, 1761, 1762, 1764, 1765, 1766, 1831, 1835, 1836, 1839, 1844, 1850, 1463], "HA": [5, 718, 6, 10, 11, 18, 27, 28, 49, 81, 82, 127, 154, 183, 185, 186, 264, 435, 459, 482, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 549, 555, 599, 705, 706, 708, 711, 712, 713, 717, 859, 861, 864, 865, 867, 869, 905, 1003, 1032, 1033, 1036, 1047, 1083, 1186, 1215, 1217, 1280, 1286, 1295, 1317, 1426, 1467, 1468, 1470, 1473, 1481, 1486, 1501, 1522, 1523, 1524, 1525, 1526, 1527, 1528, 1529, 1530, 1531, 1532, 1533, 1534, 1535, 1536, 1537, 1538, 1539, 1540, 1541, 1542, 1543, 1544, 1545, 1546, 1547, 1548, 1549, 1550, 1577, 1581, 1582, 1583, 1584, 1604, 1610, 1719, 1720, 1721, 1722, 1804, 1830, 1841, 1845, 1847, 1848, 1580], "LA": [2, 259, 4, 405, 408, 455, 685, 694, 932, 987, 1, 7, 9, 12, 15, 16, 47, 48, 51, 52, 75, 76, 77, 78, 79, 80, 83, 84, 85, 86, 87, 88, 89, 90, 109, 110, 159, 182, 195, 196, 197, 199, 200, 201, 204, 205, 206, 207, 239, 240, 241, 242, 243, 244, 245, 246, 247, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 260, 262, 266, 398, 399, 400, 402, 403, 404, 406, 407, 409, 410, 411, 412, 413, 414, 415, 417, 418, 430, 431, 449, 451, 452, 454, 456, 457, 458, 483, 484, 485, 486, 499, 502, 548, 552, 554, 564, 565, 566, 574, 575, 586, 593, 594, 595, 666, 681, 682, 683, 684, 686, 687, 688, 689, 690, 691, 692, 695, 696, 839, 840, 891, 892, 893, 894, 895, 926, 927, 928, 929, 931, 933, 934, 935, 939, 945, 946, 947, 948, 950, 951, 952, 953, 954, 956, 957, 958, 962, 968, 971, 972, 973, 974, 975, 976, 977, 978, 979, 980, 981, 982, 983, 984, 985, 986, 988, 989, 990, 991, 992, 1030, 1035, 1037, 1045, 1048, 1076, 1078, 1079, 1088, 1109, 1110, 1111, 1113, 1114, 1115, 1117, 1118, 1119, 1120, 1121, 1122, 1123, 1124, 1125, 1144, 1145, 1146, 1147, 1191, 1216, 1227, 1228, 1229, 1230, 1233, 1234, 1261, 1262, 1263, 1264, 1265, 1266, 1267, 1268, 1269, 1270, 1271, 1272, 1273, 1274, 1275, 1276, 1277, 1278, 1279, 1281, 1283, 1284, 1285, 1287, 1288, 1289, 1294, 1340, 1341, 1388, 1389, 1391, 1392, 1393, 1394, 1395, 1396, 1397, 1398, 1399, 1400, 1401, 1402, 1403, 1405, 1406, 1407, 1408, 1409, 1422, 1429, 1440, 1441, 1442, 1443, 1446, 1448, 1449, 1469, 1482, 1483, 1505, 1506, 1513, 1521, 1566, 1576, 1578, 1592, 1593, 1600, 1603, 1608, 1609, 1611, 1690, 1691, 1692, 1693, 1694, 1695, 1696, 1697, 1698, 1699, 1700, 1701, 1702, 1703, 1705, 1706, 1707, 1708, 1709, 1710, 1759, 1829, 1869, 1871, 1872, 1877, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1914, 1919, 1920, 1921, 1922, 1923, 1924, 1926, 1927, 1928, 1929, 1933, 1938, 1939, 1940, 1941, 1942, 1943, 1944, 1945, 1946, 1947, 1948, 1949, 1950, 1951, 1952, 1953, 1161, 1390, 1873], "QR": [216, 281, 608, 640, 647, 133, 214, 215, 217, 222, 283, 340, 341, 343, 432, 466, 560, 631, 632, 633, 634, 635, 636, 637, 638, 639, 641, 642, 643, 644, 645, 646, 648, 649, 650, 651, 652, 697, 736, 738, 739, 808, 809, 857, 900, 908, 949, 1068, 1069, 1132, 1169, 1306, 1309, 1343, 1357, 1421, 1424, 1485, 1619, 1647, 1648, 1649, 1650, 1651, 1652, 1653, 1654, 1655, 1656, 1657, 1658, 1659, 1740, 1744, 1745, 1793, 1794, 1832, 1889, 2014], "STN": [788, 100, 112, 113, 115, 116, 129, 130, 131, 132, 134, 137, 163, 166, 167, 330, 332, 334, 395, 397, 426, 427, 463, 467, 468, 469, 470, 471, 607, 668, 670, 671, 729, 730, 731, 787, 783, 785, 856, 941, 942, 1133, 1148, 1152, 1154, 1155, 1156, 1170, 1171, 1172, 1196, 1197, 1198, 1243, 1386, 1423, 1425, 1431, 1475, 1478, 1625, 1630, 1672, 1673, 1674, 1676, 1677, 1775, 1779, 1833, 2024, 2026, 1164, 1781], "STL": [120, 128, 160, 161, 162, 164, 165, 329, 333, 339, 342, 358, 361, 375, 464, 465, 472, 559, 605, 667, 669, 679, 780, 781, 782, 784, 786, 842, 844, 940, 1150, 1192, 1193, 1194, 1195, 1344, 1346, 1347, 1348, 1352, 1356, 1364, 1365, 1419, 1458, 1487, 1488, 1489, 1490, 1571, 1621, 1670, 1730, 1731, 1733, 1771, 1772, 1773, 1776, 1780, 1915, 1162, 1165]}

for d in depts:
	outp += """{{"model":"home.department", "pk": {0}, "fields": {{"name": "{2}", "code": "{1}"}}}}, """.format(dcounter, d, depts[d])
	dcounter += 1

for a in areas:
	outp += """{{"model": "home.area", "pk": {0}, "fields": {{"code": "{1}", "name": "{2}"}}}}, """.format(acounter, a, areas[a])
	acounter += 1

courses = json.load(open("scrape.json", "rb"))

#serialize courses
for i in range(0, len(courses)):
	course = courses[i]
	for l in course["listings"]:
		course_pks[stringify(l)] = i

sems = {"spring 2018": 0, "fall 2018": 1}
outp += """{{"model": "home.semester", "pk": {0}, "fields": {{"season": "{1}", "year": {2}}}}}, """.format(0, "s", 2018)
outp += """{{"model": "home.semester", "pk": {0}, "fields": {{"season": "{1}", "year": {2}}}}}, """.format(1, "f", 2018)

#COURSES
#make course objects
for i in range(0, len(courses)):
	course = courses[i]
	pcurr.clear()
	lcurr.clear()
	ccurr.clear()
	scurr.clear()

	for p in course["profs"]:
		outp += """{{"model": "home.professor", "pk": {0}, "fields": {{"uid": "{1}", "name": "{2}"}}}}, """.format(pcounter, p["uid"], escape(p["name"]))
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
		scurr.append(sems[s])
	#check for area
	if course["area"] == "":
		area = "null"
	else:
		area = list(areas.keys()).index(course["area"])
	outp += """{{"model": "home.course", "pk": {0}, "fields": {{"title": "{1}", "courseid": "{2}", "area": {3}, "descrip": "{4}", "professor": {5}, "listings": {6}, "prereqs": [], "classes": {7}, "semesters": {8}, "season": "{9}"}}}}, """.format(i, 
		escape(course["title"]), course["courseid"], area, escape(course["descrip"]), pcurr, lcurr, ccurr, scurr, course["term"][0][0])


#CONCENTRATIONS
concs = json.load(open("prereqs.json", "rb"))
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

	if "degree" not in conc.keys() and conc["name"] is not "A.B." and conc["name"] is not "B.S.E.":
		conc["degree"] = "AB"
	elif "degree" not in conc.keys():
		conc["degree"] = "degree"
	#add req
	outp += """{{"model": "home.concentration", "pk": {0}, "fields": {{"tipe": "{1}", "name": "{2}", "conc_code": {3}, "degree": "{4}", "year": {5}, "urls": {6}, "contacts": {7}, "req_lists": {8}}}}}, """.format(k, conc["type"], conc["name"], list(depts.keys()).index(conc["code"]), conc["degree"], conc["year"], ucurr, ccurr, rcurr)

# #SAMPLE SCHEDULES
# fil = json.load(open("sample_schedules.json", "rb"))
# saved_course_counter = 0
# plan_counter = 0
# plans = fil[0]
# print(fil[0])
# for i in plans:
# 	print(i)
# 	fall1 = plans[i]["Freshman Fall"]
# 	fall2 = plans[i]["Freshman Spring"]
# 	spring1 = plans[i]["Sophomore Fall"]
# 	spring2 = plans[i]["Sophomore Spring"]

# 	#key: COS 126 value: pk
# 	saved_course_pks = []
# 	sems = [fall1, fall2]
# 	for sem in sems:
# 		for c in sem:
# 			outp += """{{"model": "home.SavedCourse", "pk": {0}, "fields": {{"course": "{1}", "semester": "{2}"}}}}, """.format(saved_course_counter, 
# 				course_pks[c], 1)
# 			saved_course_pks.append(saved_course_counter)
# 			saved_course_counter += 1

# 	sems = [spring1, spring2]
# 	for sem in sems:
# 		for c in sem:
# 			outp += """{{"model": "home.SavedCourse", "pk": {0}, "fields": {{"course": "{1}", "semester": "{2}"}}}}, """.format(saved_course_counter, 
# 				course_pks[c], 0)
# 			saved_course_pks.append(saved_course_counter)
# 			saved_course_counter += 1



# 	outp += """{{"model": "home.plan", "pk": {0}, "fields": {{"conc": "{1}", "saved_courses": {2}}}, """.format(plan_counter, plans[i]["Concentration"], saved_course_pks)
# 	plan_counter += 1


print("[" + outp[:len(outp) - 2] + "]")


