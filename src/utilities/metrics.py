import sys
import structlinks
from structlinks.LinkedList import *

	
def findDistricts(districts):
	"""
	This function searches through a state to identify which precincts belong to which district
	inputs:
	districts - a two-dimensional array of district numbers where districts[i][j] = k means (i, j) is in district k
	
	outputs:
	precincts - a dictionary whose keys districts and whose values are lists of coordianates
	"""
	precincts = {}
	for i in range(len(districts)):
		for j in range(len(districts[0])):
			if districts[i][j] not in precincts:
				precincts[districts[i][j]] = []
			precincts[districts[i][j]].append((i, j))
	return precincts
	

	
def distance(x1, y1, x2, y2, districts):
	"""
	inputs:
	(x1, y1) and (x2, y2) are precinct locations
	districts - a two-dimensional array of the state where (i,j)=k means precinct (i,j) belongs to district k
	
	outputs:
	the distance between the two precinct locations as computed using an infinity norm
	lim (n->inf) nth root of |x1-x2|^n + |y1-y2|^n
	
	if one district or the other is not in the bounds of the state, raise error
	"""
	if districtNumber(x1, y1, districts) == -1 or districtNumber(x2,y2, districts) == -1:
		raise IndexError
	return max(abs(x1-x2), abs(y1-y2))

def compactness(districts, precincts, pow=2):
	"""
	This function computes the compactness of a possible map. It weights in favor of maps that have equal size districts;
	to change this, one would recompute "optimal" as the sum of the square roots of the district sizes.
	inputs:
	districts - two-dimensional array of districts where (i,j)=k <-> precinct (i,j) is in district k
	precincts - a dictionary whose keys are district numbers and whose values are lists of precinct coordinates
	pow - how heavily non-compact districts should be weighted. Higher pow <--> lower compactness.
	
	TODO: add output which houses compactness contributions of individual districts (memoization)
	"""
	sumOfPowers= 0
	for district in precincts:
		maxDistance = -1
		
		for d1 in precincts[district]:
			for d2 in precincts[district]:
				d = distance(d1[0], d1[1], d2[0], d2[1], districts)
				if d > maxDistance:
					maxDistance = d
		sumOfPowers+= maxDistance**pow
	numDistricts = len(precincts)
	numPrecincts = sum(len(districts[i]) for i in range(len(districts)))
	avgDistrictSize = numPrecincts / numDistricts
	
	optimal = numDistricts * (avgDistrictSize**0.5)**pow
	
	return optimal / sumOfPowers

def elongatedness(precincts):
	"""
	This function computes the elongatedness of a district. Longer/skinnier districts score worse, whereas
	more compact districts with similar lengths/widths will score better. Likely to have some reduncancy with compactness.
	
	inputs: precincts - a map whose keys are district IDs and whose values are precinct coordinates
	
	outputs: worstRatio - the worst ratio of height/width (or width/height) of any district in the state
	"""
	if len(precincts) == 0:
		return None
	worstRatio = 1
	for district in precincts:
		maxX = -1
		maxY = -1
		minX = sys.maxsize
		minY = sys.maxsize
		for d in precincts[district]:
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
		elong = min(xLen/yLen, yLen/xLen)
		if elong < worstRatio:
			worstRatio = elong
	return worstRatio
	
def districtNumber(x, y, districts):
	"""
	helper function - return the district number to which a precinct belongs
	returns -1 if the location is not part of the state
	"""
	if x<0 or y<0 or x>=len(districts) or y>=len(districts[0]):
		return -1
	return districts[x][y]

def indentedness():
	return -1
	
def puncturedness(precincts, districts):
	"""
	This function converts totalPunctures into a number that is more immediately applicable to the quality of a map.
	It returns 1 if a map is acceptable or (functionally) negative infinity otherwise.
	inputs:
	districts - two-dimensional array of districts where (i,j)=k <-> precinct (i,j) is in district k
	precincts - a dictionary whose keys are district numbers and whose values are lists of precinct coordinates
	
	outputs:
	1 if the map is not punctured, a very small number otherwise
	"""
	if totalPunctures(precincts, districts) > 0:
		return -(sys.maxsize ** 0.5)
	return 1.0
	
def totalPunctures(precincts, districts):
	"""
	This function computes the total number of punctures in a state
	inputs:
	districts - two-dimensional array of districts where (i,j)=k <-> precinct (i,j) is in district k
	precincts - a dictionary whose keys are district numbers and whose values are lists of precinct coordinates
	
	outputs:
	sum - the number of punctures in the state
	"""
	sum = 0
	for district in precincts:
		sum += numPunctures(district, precincts, districts)
	return sum

def numPunctures(district, precincts, districts):
	"""
	This function identifies the number of punctures in a given district
	inputs: 
	districts - two-dimensional array of districts where (i,j)=k <-> precinct (i,j) is in district k
	precincts - a dictionary whose keys are district numbers and whose values are lists of precinct coordinates
	district - the given district
	
	outputs:
	i - the number of punctures in the district
	"""
	# setup
	i = 0
	d = districts
	groups = {}
	for dist in precincts:
		if dist != district:
			for precinct in precincts[dist]:
				groups[precinct] = -1
	# if one district covers the whole state, then there are no punctures.
	if len(groups) == 0:
		return 0
	queue = LinkedList()
	while True:
		if len(queue) == 0:
			start = getStart(groups)
			if start == None:
				print(groups)
				return i
			isPuncture = 1
			groups[start] = i
			
		else:
			start = queue.pop(0)
		x = start[0]
		y = start[1]
		neighbors = [(x-1,y), (x,y-1), (x+1,y), (x,y+1)]
		for n in neighbors:
			neighbor = districtNumber(n[0], n[1], districts)
			if neighbor != district:
				if neighbor == -1:
					# we hit a border in the breadth first search, so the contiguous group is not a puncture
					isPuncture = 0
				elif groups[n] == -1:
					# if groups[n] != 1, we have already added it to the queue.
					# if n == -1, it is a border, and we should not explore it.
					queue.append(n)
					groups[n] = i
			# if we hit a precinct in the district in our search, we may or may not have found a puncture.
		i += isPuncture
			
	return -1
	
def getStart(groups):
	"""
	This function identifies a precinct which has not been reached by a breadth first search
	inputs:
	groups - a dictionary whose keys are precinct coordinates and whose values are the number of times that the queue has been emptied
	"""
	for key in groups.keys():
		if groups[key] == -1:
			return key
	return None

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
	return NotImplementedError
	
def getVote(x,y, votes):
	if x<0 or y<0 or x>=len(votes) or y>=len(votes[0]):
		return -1
	return votes[x][y]
	
def computeVotesEqualWeight(precincts, votes):
	"""
	This function simulates an election given a drawn map and voting outcome
	inputs:
	precincts - a dictionary whose keys are precinct coordinates and whose values are district numbers
	votes - a two-dimensional array where votes[i][j]=k means precinct (i,j) votes for k
	
	outputs:
	sums - the number of districts which vote for each candidate. Candidates are indices in "sums"
	"""
	for dist in dList:
		sums = [0, 0]
		for prec in precincts[dist]:
			sums[getVote(prec[0], prec[1], votes)] += 1
	
	return sums
	
	