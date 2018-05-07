# import re
# import json
# import copy
# import sys

# data = (json.load(open("test2.json", "r")))

# # toprint = data["d"].decode("utf-8")

# sys.stdout.write(data["d"])




def escape(s):
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
	elif s.find('"') != -1 and s.find('\\"') == -1:
		c.append(s[0:s.find('"')])
		c.append('\\"')
		c.append(s[(s.find('"')+1):])
	else:
		for char in s:
			c.append(char)
		return(''.join(c))
	return(escape(''.join(c)))


s = """Problems &amp; Methods"""
print(escape(s))