from classes.state import *
from utilities.metrics import *
from random import random
from numpy.random import normal
from utilities.utilities import *

def fitness_proportional_sampling(favored, population, num_samples):
	fitnesses = [0]*len(population)
	cum_sum = 0
	cum_fitnesses = [0]*len(population)
	samples = [0]*num_samples
	
	for i in range(len(fitnesses)):
		fitnesses[i] = compute_fitness(population[i])
		cum_sum += fitnesses[i]
		cum_fitnesses = cum_sum
	
	for i in range(num_samples):
		rand_index = random()*cum_sum
		samples[i] = population[binarySearch(cum_fitnesses, rand_index)]
	
	return samples

def geneticGerrymander(state: State, num_districts, pop_size, combination_proportion, reproductive_randomness, initial_pop_randomness, generations, recombinations,sampling_strategy=fitness_proportional_sampling, favored=1):
	# we assume that "state" is uninitialized
	"""
	inputs:
	state - the state object to be gerrymandered
	favored - the party we are trying to artificially support
	num_districts - the number of districts into which the state will be divided
	pop_size - the number of maps tracked in each iteration
	combination_proportion - the portion of districts which are taken from the parents
	reproductive_randomness - 
	initial_pop_randomness - 
	sampling_strategy - 
	generations - 
	
	output:
	state - gerrymandered state
	
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
	population = [0]*pop_size
	for i in range(pop_size):
		# new_map = randomMap(state, num_districts, initial_pop_randomness, 0)
		new_map = randomMap2(state, num_districts)
		while new_map == False:
			# can't come here with randomMap2
			# new_map = randomMap(state, num_districts, initial_pop_randomness, 0)
			new_map = randomMap2(state, num_districts)
	generation = 0
	while generation < generations:
		samples = sampling_strategy(favored, population, 2*pop_size)
		for i in range(pop_size):
			s1 = samples[int(random()*len(samples)/2)]
			s2 = samples[int(random()*len(samples)/2)]
			child = reproduce(s1, s2)
			while child == False:
				s1 = samples[int(random()*len(samples)/2)]
				s2 = samples[int(random()*len(samples)/2)]
				child = reproduce(s1, s2, combination_proportion, reproductive_randomness)
			population[i] = child
	
		# recombination
		for s in population:
			lcv = recombinations
			for i in range(lcv):
				if lcv/recombinations > 10:
				# we took too long, give up
				# TODO: parameterize
					break
				x = random()*len(s.district_matrix)
				y = random()*len(s.district_matrix[x])
				growing_dist_ID = s.getDistrictNumber(n[0], n[1])
				growing_dist = s.getDistrictByID(growing_dist_ID)
				neighbors = [(x-1,y), (x,y-1), (x+1,y), (x,y+1)]
				for m in range(3):
					rand_index1 = int(random()*4); rand_index2 = int(random()*4)
					temp = neighbors[rand_index1]; neighbors[rand_index1] = neighbors[rand_index2]; neighbors[rand_index2] = temp
				changed = False
				for n in neighbors:
					shrinking_dist_ID = s.getDistrictNumber(n[0], n[1])
					shrinking_dist = s.getDistrictByID(shrinking_dist_ID)
					if growing_dist_ID != shrinking_dist_ID:
						s.district_matrix[n[0], n[1]] = growing_dist_ID
						for m in range(len(shrinking_dist.precincts)):
							if n == shrinking_dist.precincts[m]:
								remove_index = m
						growing_dist.append(n)
						del shrinking_dist[remove_index]
						if districtIsSeparated(s, growing_dist):
							# district was separated, so we need to revert the change
							growing_dist = growing_dist[0:len(growing_dist)-1]
							shrinking_dist.append(n)
						else: 
							changed = True
				if not changed:
					lcv += 1
	
	index = 0
	max_fitness = -1
	for i in range(pop_size):
		f = compute_fitness(favored, state)
		if f > max_fitness:
			max_fitness = f
			index = i
	return population[index]
	
def neighborhoodGerrymander(state: State, num_districts, pop_size, distance, favored=1):
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
	
def reproduce(state1: State, state2: State, combination_proportion, reproductive_randomness, random_district_allowable_failures):
	district_matrix = resetMatrix(cloneMatrix(state1.voting_outcome))
	num_districts = len(state1.districts)
	num_precincts = sum(len(state1.district_matrix[i]) for i in range(len(state1.district_matrix)))
	untried = [0]*2*num_districts
	for i in range(num_districts):
		untried[i] = (1, i)
		untried[num_districts+i] = (2, i)
	precincts_assigned = 0
	districts_assigned = 0
	while precincts_assigned < combination_proportion*num_precincts and len(untried) > 0:
		index = int(random()*len(untried))
		temp = untried[index]
		state_ID = temp[0]
		district_ID = temp[1]
		del untried[index]
		if state_ID == 1:
			state = state1
		else:
			state = state2
		no_intersection = True
		for p in state.getDistrictByID(district_ID).precincts:
			if district_matrix[p[0]][p[1]] != -1:
				no_intersection = False
				break
		if no_intersection:
			for p in state.getDistrictByID(district_ID).precincts:
				district_matrix[p[0]][p[1]] = districts_assigned
			districts_assigned += 1
			precincts_assigned += len(state.getDistrictByID(district_ID).precincts)
	
	while precincts_assigned < reproductive_randomness*num_precincts:
		new_district = addRandomDistrict(district_matrix, num_precincts, num_districts, precincts_assigned, districts_assigned)
		precincts_assigned += len(new_district)
		districts_assigned += 1
		
	if addDistricts(district_matrix, num_precincts, num_districts, precincts_assigned, districts_assigned):
		child = state1.clone()
		child.instantiate(district_matrix)
		return child
	return False
		

	
	


def compute_fitness(favored, state: State, compactness_w=1, elongatedness_w=1, indentedness_w=1, puncturedness_w=1, separatedness_w=1, voting_outcome_w=5, compactness_pow=2.0):
	"""
	compactness
	elongatedness
	indentedness
	puncturedness
	separatedness
	voting_outcome
	TODO: include nonlinear voting outcome fitness (e.g. is 81% better than 80% by the same amount that 51% is better than 50%?)
	"""
	votes = computeVotesEqualWeight(state)
	proportion = votes[favored] / (votes[favored] + votes[1 - favored])
	denom = compactness_w + elongatedness_w + indentedness_w + puncturedness_w + separatedness_w + voting_outcome_w
	return compactness_w*compactness(state, compactness_pow) + elongatedness_w*elongatedness(state) + indentedness_w*indentedness(state) + puncturedness_w*puncturedness(state) + separatedness_w*separatedness(state) + voting_outcome_w*proportion / denom
	

def randomMap2(state: State, num_districts):
	district_matrix = cloneMatrix(state.voting_outcome)
	resetMatrix(district_matrix)
	assigned = []
	unassigned = []
	for i in range(len(state.voting_outcome)):
		for j in range(len(state.voting_outcome[i])):
			unassigned.append((i,j))
	candidates = []
	for i in range(num_districts):
		precinct = unassigned[int(random()*len(unassigned))]
		x = precinct[0]; y = precinct[1]
		district_matrix[x][y] = i
		neighbors = [(x-1,y),(x,y-1),(x+1,y),(x,y+1)]
		for n in neighbors:
			if is_unmatched(n, district_matrix) and not n in candidates and not n in assigned:
				candidates.append(n)
	while candidates != []:
		candidate_index = int(random()*len(candidates))
		precinct = candidates[candidate_index]
		x = precinct[0]; y = precinct[1]
		neighbors = [(x-1,y),(x,y-1),(x+1,y),(x,y+1)]
		district_options = []
		for n in neighbors:
			if is_matched(n, district_matrix):
				if not district_matrix[n[0]][n[1]] in district_options:
					district_options.append(district_matrix[n[0]][n[1]])
			elif is_unmatched(n, district_matrix):
				candidates.append(n)
		district_matrix[x][y] = district_options[int(random()*len(district_options))]
		del candidates[candidate_index]
		assigned.append(precinct)
	
	return district_matrix
		
		
	
	
def randomMap(state: State, num_districts, randomness=0.3, tolerable_failures=10):
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
	if tolerable_failures < 0:
		return False
	district_matrix = cloneMatrix(state.voting_outcome)
	num_precincts = 0
	for i in range(len(district_matrix)):
		for j in range(len(district_matrix[i])):
			district_matrix[i][j] = -1
			num_precincts += 1
	districts_assigned = 0
	precincts_assigned = 0
	while(precincts_assigned < randomness*num_precincts):
		backup_copy = cloneMatrix(district_matrix)
		distr = addRandomDistrict(district_matrix, num_precincts, num_districts, precincts_assigned, districts_assigned)
		if not distr:
			# TODO: decrement tolerable failures, try again
			return False
		precincts_assigned += len(distr)
		districts_assigned += 1
	print("districts assigned", districts_assigned)
	# while districts_assigned < num_districts:
	# 	distr_size = addDistrict(state, district_matrix, num_precincts, num_districts):
	#	if distr_size == False:
	#		return False
	#	precincts_assigned += distr_size
	#	districts_assigned += 1
	print(district_matrix)
	print(num_precincts)
	print(num_districts)
	print(precincts_assigned)
	print(districts_assigned)
	ret = addDistricts(district_matrix, num_precincts, num_districts, precincts_assigned, districts_assigned)
	print(ret)
	if not ret:
		print("aaaaaaaaaaaaaaaaaaaaa")
		return randomMap(state, num_districts, randomness, tolerable_failures - 1)
	print("bbbbbbbbbbbb")
	
	clone = state.clone()
	clone.instantiate(district_matrix)
	
	return clone
	
def addRandomDistrict(district_matrix, num_precincts, num_districts, precincts_assigned, districts_assigned):
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
	while len(candidates) > 0 and remaining > 0:
		remaining -= 1
		rand_index = int(random()*len(candidates))
		cur = candidates[rand_index]
		district_list.append(cur)
		del candidates[rand_index]
		x = cur[0]; y = cur[1]
		district_matrix[x][y] = districts_assigned
		neighbors = [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]
		for n in neighbors:
			if is_unmatched(n, district_matrix) and not n in candidates and not n in district_list:
				candidates.append(n)
	return district_list
	
	
def addDistricts(district_matrix, num_precincts, num_districts, precincts_assigned, districts_assigned):
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
	original_district_matrix = cloneMatrix(district_matrix)
	
	if districts_assigned == num_districts:
		print("districts_assigned", districts_assigned)
		print("num_districts", num_districts)
		print("precincts_assigned", precincts_assigned)
		print("num_precincts", num_precincts)
		# shouldn't be a way for num_precincts to differ from precincts_assigned, but just in case
		return precincts_assigned == num_precincts
	goal_size = (num_precincts - precincts_assigned) / (num_districts - districts_assigned)
	print("goal size", goal_size)
	print("num_districts", num_districts)
	
	groups = contiguousGroups(is_unmatched, district_matrix)
	groups.sort(key=len)
	accrued = 0 # TODO: forgot what this was for
	while len(groups) > 0 and len(groups[0]) <= goal_size:
		precincts_assigned += len(groups[0])
		update_district_matrix(district_matrix, groups[0], districts_assigned)
		districts_assigned += 1
		del groups[0]
		if num_districts == districts_assigned:
			print("precincts_assigned", precincts_assigned)
			return district_matrix
		goal_size = (num_precincts - precincts_assigned) / (num_districts - districts_assigned)

	new_district = addRandomDistrict(district_matrix, num_precincts, num_districts, precincts_assigned, districts_assigned)
	if not new_district:
		return False
	precincts_assigned += len(new_district)
	
	new_groups = contiguousGroups(is_unmatched, district_matrix)
	merges = len(new_groups) + districts_assigned - num_districts
	while merges > 0:
		"""
		choose random place in new district
		choose random available adjacent square
		expand in that direction
		"""
		if(type(new_district) is not list):
			print(new_district)
		for i in range(len(new_district)):
			x = new_district[i][0]
			y = new_district[i][1]
			neighbors = [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]
			start = -1
			for n in neighbors:
				if is_unmatched(n, district_matrix):
					start = n
					break
			if start != -1:
				group = bfs(start, is_unmatched, district_matrix)
				for prec in group:
					district_matrix[prec[0]][prec[1]] = districts_assigned
				precincts_assigned += len(group)
				
				break
		merges = merges - 1
	districts_assigned += 1
	return addDistricts(district_matrix, num_precincts, num_districts, precincts_assigned, districts_assigned)
		
		

def update_district_matrix(district_matrix, district_list, district_ID):
	for pos in district_list:
		x = pos[0]; y = pos[1]
		district_matrix[x][y] = district_ID
	
def is_unmatched(ordered_pair, district_matrix):
	x = ordered_pair[0]; y = ordered_pair[1]
	if x<0 or y<0 or x>=len(district_matrix) or y>=len(district_matrix[x]):
		return False
	return district_matrix[x][y] == -1
	
def is_matched(ordered_pair, district_matrix):
	x = ordered_pair[0]; y = ordered_pair[1]
	if x<0 or y<0 or x>=len(district_matrix) or y >=len(district_matrix[x]):
		return False
	return district_matrix[x][y] != -1
	

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
	return mean + normal(0)*sd

def getStart(fun, matr):
	for i in range(len(matr)):
		for j in range(len(matr[i])):
			if fun((i, j), matr):
				return (i, j)
	return False
	
def contiguousGroups(fun, matr):
	groups = []
	start = getStart(fun, matr)
	newMatr = cloneMatrix(matr)
	while not not start:
		group = bfs(start, fun, newMatr)
		groups.append(group)
		for pos in group:
			newMatr[pos[0]][pos[1]] = 1
		start = getStart(fun, newMatr)
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
			if (n not in queue) and (n not in group) and fun(n, matr):
				queue.append(n)
	return group

def binarySearch(cum_fitnesses, rand_value):
	if rand_value < cum_fitnesses[0]:
		return 0
	min = 0
	max = len(cum_fitnesses) - 1
	mid = round((min + max)/2 + 0.00001)
	while cum_fitnesses[mid] < rand_value or cum_fitnesses[mid - 1] > rand_value:
		mid = round((min + max)/2 + 0.00001)
		if rand_value < cum_fitnesses[mid]:
			max = mid
		else:
			min = mid
	return mid

def resetMatrix(matr):
	for i in range(len(matr)):
		for j in range(len(matr[i])):
			matr[i][j] = -1
	return matr