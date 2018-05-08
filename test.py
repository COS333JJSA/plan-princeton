import json

result_load = json.load(open("partial_response.json", "r"))
print(result_load['000004'])