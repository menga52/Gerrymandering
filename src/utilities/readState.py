state1 = []
for i in range(10):
	state1.append([i]*10)
	
def readState(string: str):
	if string.find(".txt") == -1:
		string +=  ".txt"
	districts = []
	votes = -1
	try:
		fileref = open(string)
	except FileNotFoundError:
		print("file not found :(")
		return
	except:
		print("error")
		return
	for line in fileref:
		row = []
		for word in line.split():
			row.append(word)
		if row == []:
			votes = []
		if votes == -1:
			districts.append(row)
		else:
			if row == []:
				continue
			votes.append(row)
		
	return districts, votes