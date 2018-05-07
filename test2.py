# import re
# import json
# import copy
# import sys

# data = (json.load(open("test2.json", "r")))

# # toprint = data["d"].decode("utf-8")

# sys.stdout.write(data["d"])


import re

def escape(s):
	print(s)
	print()
	c = []
	if s == None:
		return ""
	if s.find('&#39;') != -1:
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
	elif re.search(r"[A-Za-z\s\.,\?!]\"", s) != None:
		st = re.search(r"[A-Za-z\s\.,\?!]\"", s).end()
		c.append(s[0:st-1])
		c.append('\\"')
		c.append(s[(st):])
	else:
		for char in s:
			c.append(char)
		return(''.join(c))
	return(escape(''.join(c)))


s = "\"The Harlem Renaissance (HR) of the 1920s\" is most often depicted as \"the flowering of African American arts and literature.\" It can also be characterized as a period when diverse forms of African American religious expressions, ideologies, and institutions emerged. This course explores the literature of the Harlem Renaissance, particularly the writings of Langston Hughes, to understand the pivotal intersection of race and religion during this time of black \"cultural production.\""
print(escape(s))

# elif s.find('"') != -1 and s.find('\\"') == -1: