import re
import json
import copy
import sys

data = (json.load(open("test2.json", "rb")))

# toprint = data["d"].decode("utf-8")

print(data["d"])