  first = True
  TERM_CODES = {1192: "fall 2018", 1184: "spring 2018", 1182: "fall 2017", 1174: "spring 2017"}
  courses = {{"courseid": "1", "prof": "ted"}, {"courseid": "2", "prof": "ted1"}}
  result = {}
  for term in TERM_CODES:
    oneterm = []
    oneterm_ids = []
    TERM_CODE = term

    for course in courses:
      if (course["courseid"] not in oneterm_ids):
        if (course["courseid"] in result):
          result.get(course["courseid"])["term"].append(TERM_CODES[term])
          # json.dump(course["courseid"], sys.stdout)
        course["term"].append(TERM_CODES[term])
        oneterm.append(course)
        oneterm_ids.append(course["courseid"])
        json.dump(course["courseid"], sys.stdout)

        # json.dump(course["courseid"], sys.stdout)

    for c in oneterm:
      result[c["courseid"]] = c
    print(result)