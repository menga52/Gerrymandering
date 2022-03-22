import sys

d = -1
v = -1
dList = -1
districtPrecincts = -1
def setState(districts, votes):
	global d, v, dList, districtPrecincts
	d = districts
	v = votes
	dList, districtPrecincts = findDistricts(districts)
	
def findDistricts(districts):
	unique = []
	precincts = {}
	for i in range(len(districts)):
		for j in range(len(districts[0])):
			if districts[i][j] not in unique:
				unique.append(districts[i][j])
				precincts[districts[i][j]] = []
			precincts[districts[i][j]].append((i, j))
	return unique, precincts
	
def distance(x1, y1, x2, y2):
	"""
	inputs:
	(x1, y1) and (x2, y2) are precinct locations
	
	outputs:
	the distance between the two precinct locations as computed using an infinity norm
	lim (n->inf) nth root of |x1-x2|^n + |y1-y2|^n
	"""
	return max(abs(x1-x2), abs(y1-y2))

def compactness():
	global dList, districtPrecincts
	sumOfSquares = 0
	for district in dList:
		maxDistance = -1
		
		for d1 in districtPrecincts[district]:
			for d2 in districtPrecincts[district]:
				d = distance(d1[0], d1[1], d2[0], d2[1])
				if d > maxDistance:
					maxDistance = d
		sumOfSquares += maxDistance**2
	numDistricts = len(dList)
	numPrecincts = sum(len(districts[i]) for i in range(len(districts)))
	avgDistrictSize = numPrecincts / numDistricts
	
	optimal = numDistricts * avgDistrictSize**0.5
	
	return optimal / sumOfSquares	

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