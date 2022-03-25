state1 = []
for i in range(10):
	state1.append([i]*10)
	
def openFile(string: str):
	"""
	helper function - opens a file given a file name
	"""
	if string.find(".txt") == -1:
		string +=  ".txt"
	try:
		fileref = open(string)
	except FileNotFoundError:
		print("file not found :(")
		return -1
	return fileref
	
def readState(string: str):
	"""
	This function parses a file into a 2D array representation of a voting outcome
	inputs:
	string - filename (with or without .txt)
	outputs:
	districts - a 2D array describing which precincts belong to which (of potentially many) districts
	votes - a 2D array of votes (binary)
	"""
	fileref = openFile(string)
	if fileref == -1:
		return
	districts = []
	votes = -1
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
	
def readStateWithoutDistricts(string: str):
	"""
	This function parses a file into a 2D array representation of a voting outcome
	inputs:
	string - filename (with or without .txt)
	outputs:
	votes - a 2D array of votes
	"""
	fileref = openFile(string)
	if fileref == -1:
		return -1
	votes = []
	for line in fileref:
		row = []
		for word in line.split():
			row.append(word)
		votes.append(row)
	return votes
	
	
