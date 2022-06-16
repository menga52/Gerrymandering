import sys
import structlinks
from structlinks.LinkedList import *
from classes.state import *

	
def distance(x1, y1, x2, y2, district_matrix):
	"""
	inputs:
	(x1, y1) and (x2, y2) are precinct locations
	districts - a two-dimensional array of the state where (i,j)=k means precinct (i,j) belongs to district k
	
	outputs:
	the distance between the two precinct locations as computed using an infinity norm
	lim (n->inf) nth root of |x1-x2|^n + |y1-y2|^n
	
	if one district or the other is not in the bounds of the state, raise error
	"""
	dim1 = len(district_matrix)
	if x1<0 or x1>=dim1 or x2<0 or x2>=dim1 or y1<0 or y2<0:
		raise IndexError
	# if districtNumber(x1, y1, district_matrix) == -1 or districtNumber(x2,y2, district_matrix) == -1:
		# raise IndexError
	elif y1>=len(district_matrix[x1]) or y2>=len(district_matrix[x2]):
		raise IndexError
	return max(abs(x1-x2), abs(y1-y2))

def compactness(state: State, pow=2):
	"""
	This function computes the compactness of a possible map. It weights in favor of maps that have equal size districts;
	to change this, one would recompute "optimal" as the sum of the square roots of the district sizes.
	inputs:
	districts - two-dimensional array of districts where (i,j)=k <-> precinct (i,j) is in district k
	precincts - a dictionary whose keys are district numbers and whose values are lists of precinct coordinates
	pow - how heavily non-compact districts should be weighted. Higher pow <--> lower compactness.
	
	TODO: add output which houses compactness contributions of individual districts (memoization)
		  add argument for memoized district compactness values
	"""
	if not state.instantiated:
		print("should not compute compactness of uninstantiated state")
		raise ValueError
	district_matrix = state.district_matrix
	sumOfPowers= 0
	for district in state.districts:
		maxDistance = -1
		
		for p1 in district.precincts:
			for p2 in district.precincts:
				d = distance(p1[0], p1[1], p2[0], p2[1], district_matrix)
				if d > maxDistance:
					maxDistance = d
		sumOfPowers += maxDistance**pow
	numDistricts = len(state.districts)
	numPrecincts = sum(len(district_matrix[i]) for i in range(len(district_matrix)))
	avgDistrictSize = numPrecincts / numDistricts
	
	optimal = numDistricts * (avgDistrictSize**0.5)**pow
	
	return optimal / sumOfPowers

def elongatedness(state: State):
	"""
	This function computes the elongatedness of a district. Longer/skinnier districts score worse, whereas
	more compact districts with similar lengths/widths will score better. Likely to have some reduncancy with compactness.
	
	inputs: precincts - a map whose keys are district IDs and whose values are precinct coordinates
	
	outputs: worstRatio - the worst ratio of height/width (or width/height) of any district in the state
	
	# TODO: add arguments to make the function customizable
	"""
	if len(state.districts) == 0:
		return None
	worstRatio = 1
	for district in state.districts:
		maxX = -1
		maxY = -1
		minX = sys.maxsize
		minY = sys.maxsize
		
		for p in district.precincts:
			if maxX < p[0]:
				maxX = p[0]
			if minX > p[0]:
				minX = p[0]
			if maxY < p[1]:
				maxY = p[1]
			if minY > p[1]:
				minY = p[1]
		xLen = maxX - minX + 1
		yLen = maxY - minY + 1
		# xLen = district.maxX - district.minX + 1
		# yLen = district.maxY - district.minY + 1
		elong = min(xLen/yLen, yLen/xLen)
		if elong < worstRatio:
			worstRatio = elong
	return worstRatio
	
def districtNumber(x, y, district_matrix):
	"""
	helper function - return the district number to which a precinct belongs
	returns -1 if the location is not part of the state
	"""
	if x<0 or y<0 or x>=len(district_matrix) or y>=len(district_matrix[x]):
		return -1
	return district_matrix[x][y]

def indentedness(state: State):
	return -1
	
def puncturedness(state: State):
	"""
	This function converts totalPunctures into a number that is more immediately applicable to the quality of a map.
	It returns 1 if a map is acceptable or (functionally) negative infinity otherwise.
	inputs:
	districts - two-dimensional array of districts where (i,j)=k <-> precinct (i,j) is in district k
	precincts - a dictionary whose keys are district numbers and whose values are lists of precinct coordinates
	
	outputs:
	1 if the map is not punctured, a very small number otherwise
	# TODO: compute nonbinary composite metric
	"""
	
	if totalPunctures(state) > 0:
		return -(sys.maxsize ** 0.5)
	return 1.0
	
def totalPunctures(state: State):
	"""
	This function computes the total number of punctures in a state
	inputs:
	districts - two-dimensional array of districts where (i,j)=k <-> precinct (i,j) is in district k
	precincts - a dictionary whose keys are district numbers and whose values are lists of precinct coordinates
	
	outputs:
	sum - the number of punctures in the state
	"""
	sum = 0
	for district in state.districts:
		sum += numPunctures(district, state)
	return sum

def numPunctures(district, state: State):
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
	# d = state.district_matrix
	groups = {}
	for dist in state.districts:
		if dist.id != district.id:
			for precinct in dist.precincts:
				groups[precinct] = -1
	# if one district covers the whole state, then there are no punctures.
	if len(groups) == 0:
		return 0
	queue = LinkedList()
	while True:
		if len(queue) == 0:
			start = getStart(groups)
			if start == None:
				return i
			isPuncture = 1
			groups[start] = i
			
		else:
			start = queue.pop(0)
		x = start[0]
		y = start[1]
		neighbors = [(x-1,y), (x,y-1), (x+1,y), (x,y+1)]
		for n in neighbors:
			neighbor_district_id = districtNumber(n[0], n[1], state.district_matrix)
			if neighbor_district_id != district.id:
				if neighbor_district_id == -1:
					# we hit a border in the breadth first search, so the contiguous group is not a puncture
					isPuncture = 0
				elif groups[n] == -1:
					# if groups[n] != -1, we have already added it to the queue.
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
	
def separatedness(state: State):
	"""
	input:
	state - state object in question
	
	output:
	1 if map is not separated, -(sys.maxsize**0.5) otherwise
	"""
	for district in state.districts:
		if districtIsSeparated(state, district):
			return -(sys.maxsize**0.5)
	return 1.0

def districtIsSeparated(state: State, district):
	"""
	state - state object in question
	district - district object being tested
	output:
	True if the district is disjoint (discontinuous, disallowing neighbors via corners), False otherwise
	"""
	if len(district.precincts) == 0:
		return False
	queue = LinkedList()
	queue.append(district.precincts[0])
	checked = [district.precincts[0]]
	while len(queue) != 0:
		start = queue.pop(0)
		x = start[0]
		y = start[1]
		neighbors = [(x-1,y), (x,y-1), (x+1,y), (x,y+1)]
		for n in neighbors:
			if n in checked:
				continue
			n_id = districtNumber(n[0], n[1], state.district_matrix)
			if n_id == district.id:
				queue.append(n)
				checked.append(n)
	
	return len(checked) != len(district.precincts)

	"""
	for each district
		breadth first search
		if search doesn't reach all precincts in district, return false
	return true
	"""
	return NotImplementedError
	
def getVote(x,y, votes):
	if x<0 or y<0 or x>=len(votes) or y>=len(votes[x]):
		return -1
	return votes[x][y]
	
def computeVotesEqualWeight(state: State):
	"""
	This function simulates an election given a drawn map and voting outcome
	inputs:
	precincts - a dictionary whose keys are precinct coordinates and whose values are district numbers
	votes - a two-dimensional array where votes[i][j]=k means precinct (i,j) votes for k
	
	outputs:
	sums - the number of districts which vote for each candidate. Candidates are indices in "sums"
	"""
	votes = [0, 0]
	for district in state.districts:
		sums = [0, 0]
		for prec in district.precincts:
			sums[getVote(prec[0], prec[1], state.voting_outcome)] += 1
		if sums[0]>sums[1]:
			votes[0] += 1
		elif sums[1]>sums[0]:
			votes[1] += 1
	return votes
	
