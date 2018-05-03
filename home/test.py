reqs = ["General Chemistry", 2, ["Differential and Integral Calculus", 2, ["Calculus II", "Calculus I"]]]
level_one = []
level_two = []
level_three = []
level_four = []
level_one_nums = []
level_two_nums = []
level_three_nums = []
counter1 = 0
counter2 = 0
counter3 = 0

for r in reqs:
	if type(r) != list:
		if type(r) != int:
			level_one.append(r)
		else:
			level_one_nums.append(r)
		counter1 += 1
	else:
		for r2 in r:
			temp2 = []
			temp3 = [[[]]]
			counter3 = 0
			if type(r2) != list:
				if type(r2) != int:
					temp2.append(r2)
				else:
					level_two_nums.append(r2)
			else:
				for r3 in r2:
					if type(r3) != list:
						if type(r3) != int:
							temp3[counter3].append(r3)
							counter3 += 1
						else:
							level_three_nums.append(r3)
						counter3 += 1
					else:
						for r4 in r:
							level_four.append(r4)
					level_three.append(temp3)
			level_two.append(temp2)


print(level_one)
print(level_one_nums)
print(level_two)
print(level_two_nums)
print(level_three)
print(level_three_nums)