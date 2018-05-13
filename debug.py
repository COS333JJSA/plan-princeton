import sys
import string

if __name__ == "__main__":
  result = {126: {"courseid": 126, "term": []}}
  courses = [{"courseid": 126, "term": []}, {"courseid": 126, "term": []}, {"courseid": 217, "term": []}]

  TERM_CODES = {1192: "fall 2018", 1184: "spring 2018", 1182: "fall 2017", 1174: "spring 2017"}

  first = True
  for term in TERM_CODES:
    print ("TERM: " + str(term))
    oneterm_ids = []
    TERM_CODE = term

    for course in courses:
      if (course["courseid"] not in oneterm_ids):
        if (course["courseid"] in result):
          print (course["courseid"])
          result.get(course["courseid"])["term"].append(TERM_CODES[term])
          # json.dump(course["courseid"], sys.stdout)
        else:
          course["term"].append(TERM_CODES[term])
          result[course["courseid"]] = course
        
        oneterm_ids.append(course["courseid"])

      print (result)
        # course has already been seen this term - ignore
        #json.dump(course["courseid"], sys.stdout)

    # for c in oneterm:
    #   result[c] = c["term"].append()
  print ("result")
  print (result)
  print ("courses")
  print (courses)
# # printing
#   first = True
#   for c in result:
#     if first:
#       first = False
#       print('[')
#     else:
#       print(',')
#     json.dump(result[c["courseid"]], sys.stdout)
#   print(']')