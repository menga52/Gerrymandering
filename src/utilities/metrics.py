import sys
import structlinks
from structlinks.LinkedList import *
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
	maxX = -1
	maxY = -1
	minX = len(districtPrecincts)
	minY = len(districtPrecincts[0])
	for d in districtPrecincts:
		if maxX < d[0]:
			maxX = d[0]
		if minX > d[0]:
			minX = d[0]
		if maxY < d[1]:
			maxY = d[1]
		if minY > d[1]:
			minY = d[1]
	xLen = maxX - minX + 1
	yLen = maxY - minY + 1
	return min(xLen/yLen, yLen/xLen)
	
def districtNumber(x, y):
	"""
	helper function - return the district number to which a precinct belongs
	returns -1 if the location is not part of the state
	"""
	if x<0 or y<0 or x>=len(districtPrecints) or y>=len(districtPrecincts[0]):
		return -1
	return districts[x][y]

def indentedness():
	return -1

def numPunctures(district):
	"""
	i=0
	while there are remain unchecked precincts outside the district do:
		create new list
		i+=1
		breadth first search to find all neighboring precincts outside the district starting from an unchecked district
		return i - 1
	"""
	return -1

def numComponents():
	"""
	probably unnecessary
	"""
	return -1

def isSeparated():
	"""
	for each district
		breadth first search
		if search doesn't reach all precincts in district, return false
	return true
	"""
	return -1
	
def getVote(x,y):
	if x<0 or y<0 or x>=len(districtPrecints) or y>=len(districtPrecincts[0]):
		return -1
	return votes[x][y]
	
def computeVotesEqualWeight():
	# if perspective != 0 and perspective != 1:
	#	raise ValueError("perspective should be one or zero")
	for dist in dList:
		sums = [0, 0]
		for prec in districtPrecincts[dist]:
			sums[getVote(prec[0], prec[1])] += 1
	
	return sums
	
	