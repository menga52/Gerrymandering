from classes.state import *
from utilities.metrics import *
from random import random
from numpy.random import normal

def geneticGerrymander(state: State, favored=1, num_districts, pop_size):
	# we assume that "state" is uninitialized
	"""
	inputs:
	state - the state object to be gerrymandered
	favored - the party we are trying to artificially support
	pop_size - the number of maps tracked in each iteration
	num_districts - the number of districts into which the state will be divided
	
	output:
	state - gerrymandered state (
	
	strategy: 
	find initial maps - randomly generate until we have some set number pop_size of legal maps
	compute fitness of each map
	repeat:
		
		until pop_size valid maps:
			sample twice from population
			take one district from each until no more are possible (probably fewer times than this to create higher rate of validity)
			fill in remaining districts randomly
		new population = result
	"""
	return NotImplementedError
	
	def neighborhoodGerrymander(state: State, favored=1, num_districts, pop_size, distance):
	"""
	inputs:
	state - the state object to be gerrymandered
	favored - the party we are trying to artificially support
	pop_size - the number of maps tracked in each iteration
	num_districts - the number of districts into which the state will be divided
	distance - the maximum number of random switches to be carried out in switching phase
	
	Note that the distance between two maps is half the number of precincts that differ between the two maps.
		to compute it, we would iterate through each map and compute, for each map, the number of precincts with
		differing district IDs, add them up, and divide by two. Because districts need not be constant size, 
		distances between maps need not be whole numbers.
		
		We define distance in this way so that we can construct a map that has distance N from a given district
		by swapping N precincts in each district
	"
	
	strategy:
	find initial maps
	repeat
	"""
	return NotImplementedError
	
def randomMap(state: State, num_districts, randomness, tolerable_failures):
	"""
	inputs:
	state - the state object being gerrymandered
	num_districts - the number of districts into which the state will be divided
	randomness - a float in (0,1). Greater randomness will result in districts more randomly
		assigned; lower randomness will result in fewer failed attempts. 
	tolerable_failures - the number of failed addDistrict (or addRandomDistrict) calls
		that should be tolerated before declaring failure
	
	output:
	clone - a clone of the state object passed in with assigned districts
		OR: False, if failed.
	instantiates a state with a random contiguous assignment of precincts to districts
	
	TODO: use number of allowable failure input
	"""
	if tolerable_failures < 1:
		return False
	district_matrix = cloneMatrix(state.voting_outcome)
	num_precincts = 0
	for i in range(len(district_matrix)):
		for j in range(len(district_matrix[i])):
			district_matrix[i][j] = -1
			num_precincts += 1
	districts_assigned = 0
	precincts_assigned = 0
	while(districts_assigned < randomness*num_districts):
		distr = addRandomDistrict(state, district_matrix, num_precincts, num_districts, precincts_assigned, districts_assigned):
		if distr_size == False:
			return False
		precincts_assigned += len(distr)
		districts_assigned += 1
	
	# while districts_assigned < num_districts:
	# 	distr_size = addDistrict(state, district_matrix, num_precincts, num_districts):
	#	if distr_size == False:
	#		return False
	#	precincts_assigned += distr_size
	#	districts_assigned += 1
	if not addDistricts(state, district_matrix, num_precincts, num_districts, precincts_assigned, districts_assigned):
		randomMap(state, num_districts, randomness, tolerable_failures - 1
	
	clone = state.clone()
	clone.instantiate(district_matrix)
	
	return NotImplementedError
	# return clone
	
def addRandomDistrict(state: State, district_matrix, num_precincts, num_districts, precincts_assigned, districts_assigned):
	"""
	inputs:
	state - the state object being gerrymandered
	district_matrix - the gerrymander in progress
	num_precincts - the number of precincts in the state
	num_districts - the number of districts needed
	precincts_assigned - the number of precincts which have already been assigned to districts
	districts_assigned - the number of districts which have already been assigned in this map
	
	output:
	mutates district_matrix
	returns the new district
	
	after calling, districts_assigned and precincts_assigned should be updated
	"""
	goal_size = (num_precincts - precincts_assigned) / (num_districts - districts_assigned)
	if goal_size < 1:
		return False
	candidates = []
	cur = findAvailablePrecinct(district_matrix)
	candidates.append(cur)
	district_list = []
	
	remaining = max(1, int(normalSample(goal_size+1.5, goal_size**(1/3)))) # TODO: choose the max size of the district from normal distribution
	while len(candidates) > 0 && remaining > 0:
		remaining -= 1
		rand_index = int(random()*len(candidates))
		cur = candidates[rand_index]
		district_list.append(cur)
		del candidates[rand_index]
		x = cur[0]; y = cur[1]
		district_list.append(cur)
		district_matrix[x][y] = districts_assigned
		neighbors = [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]
		for n in neighbors:
			if is_unmatched(n):
				candidates.append(n)
	return district_list
	
	
def addDistricts(state: State, district_matrix, num_precincts, num_districts, precincts_assigned, districts_assigned):
	"""
	approach: 
		first, check to see if done
		compute groups with breadth-first search
		if too many groups (num groups > num_districts - districts_assigned), fail
		compute goal_size
		compute min size of group
		while min size < goal_size
			assign min size group as district
			recompute goal_size and min size
		
		add random district (call)
		recompute groups
		if too many groups:
			repeat:
				breadth first search from a random position in new district, add all to new district
				update groups
			until num groups small enough
		recursive call
	"""
	if districts_assigned == num_districts:
		# shouldn't be a way for num_precincts to differ from precincts_assigned, but just in case
		return precincts_assigned == num_precincts
	goal_size = (num_precincts - precincts_assigned) / (num_districts - districts_assigned)
	
	groups = contiguousGroups(is_unmatched, district_matrix)
	groups.sort(key=len)
	accrued = 0 # TODO: forgot what this was for
	while len(groups) > 0 && len(groups[0]) < goal_size:
		precincts_assigned += len(groups[0])
		update_district_matrix(district_matrix, groups[0], districts_assigned)
		districts_assigned += 1
		del groups[0]
		goal_size = (num_precincts - precincts_assigned) / (num_districts - districts_assigned)
	
	new_district = addRandomDistrict(state, district_matrix, num_precincts, num_districts, precincts_assigned, districts_assigned)
	new_groups = contiguousGroups(is_unmatched, district_matrix)
	merges = len(new_groups) + districts_assigned - num_districts
	while merges > 0:
		"""
		choose random place in new district
		choose random available adjacent square
		expand in that direction
		"""
		for i in range(len(new_district)):
			x = new_district[i][0]
			y = new_district[i][1]
			neighbors = [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]
			start = -1
			for n in neighbors:
				if is_unmatched(n):
					start = n
					break
			if start != -1:
				group = bfs(start, is_unmatched, district_matrix)
				for prec in group:
					district_matrix[prec[0], prec[1]] = districts_assigned
				precincts_assigned += len(group)
				
				break
	districts_assigned += 1
	return addDistricts(district_matrix, num_precincts, num_districts, precincts_assigned, districts_assigned)
		
		

def update_district_matrix(district_matrix, district_list, district_ID):
	for pos in district_list:
		x = pos[0]; y = pos[1]
		district_matrix[x][y] = district_ID
	
def is_unmatched(ordered_pair):
	x = ordered_pair[0]; y = ordered_pair[1]
	if x<0 or y<0 or x>=len(district_matrix) or y>=len(district_matrix[x]):
		return False
	return district_matrix[x][y] == -1
	

def findAvailablePrecinct(district_matrix):
	"""
	This function chooses a random precinct to constitute the 'start' of the next random district
	
	inputs:
	district_matrix - the gerrymander in progress
	output:
	(i,j) coordinates of first precinct in a new random precinct
	
	potential problem: chooses non-uniformly in non-rectangular districts
	"""
	timeout = 1000
	while timeout > 0:
		i = int(random()*len(district_matrix))
		j = int(random()*len(district_matrix[i]))
		if district_matrix[i][j] == -1:
			return (i, j)
	return False
	
def normalSample(mean, sd):
	#TODO: check math
	return mean + normal*sd

def getStart(fun, matr):
	for i in range(len(matr)):
		for j in range(len(matr[i])):
			if fun(matr[i][j]):
				return (i, j)
	return False
	
def contiguousGroups(fun, matr):
	groups = []
	start = getStart(fun, matr)
	while not not start:
		group = bfs(start, fun, matr)
		groups.append(group)
	return groups

def bfs(start, fun, matr):
	queue = LinkedList()
	queue.append(start)
	group = []
	while not len(queue)==0:
		cur = queue.pop(0)
		group.append(cur)
		x = cur[0]
		y = cur[1]
		neighbors = [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]
		for n in neighbors:
			if fun(n):
				queue.append(n)
	return group
	