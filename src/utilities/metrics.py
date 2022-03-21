d = -1
v = -1
dList = -1
def setState(districts, votes):
	global d, v
	d = districts
	v = votes
	dList = findDistricts(districts)
	
def findDistricts(districts):
	unique = []
	for i in range(len(districts)):
		for j in range(len(districts[0])):
			if districts[i][j] not in unique:
				unique.append(districts[i][j])
	return unique

def compactness():
	return -1	

def elongatedness():
	return -1

def indentedness():
	return -1

def numPunctures():
	return -1

def numComponents():
	return -1

def isSeparated():
	return -1