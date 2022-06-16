from classes.state import *
from utilities.metrics import *
from random import random
from numpy.random import normal
from classes.state import cloneMatrix
from utilities.utilities import *

def fitness_proportional_sampling(population, num_samples, fitness_function=compute_fitness, favored=1):
	"""
	choose the parents for the next generation based on a supplied fitness function
	population - a list of state objects from which parents will be chosen
	num_samples - the number of parents to be selected
	fitness_function - a function which defines the quality of a district map in a state
	favored - the party we desire to favor
	"""
	fitnesses = [0]*len(population) # the fitness of each individual in population
	cum_sum = 0 # the intermediate cumulative sum of fitnesses
	cum_fitnesses = [0]*len(population) # a list of the intermediate cumulative fitnesses
	samples = [0]*num_samples # the output; those individuals selected for reproduction
	
	for i in range(len(fitnesses)):
		# compute the fitness of individual i
		fitnesses[i] = fitness_function(favored, population[i])
		# set the cumulative sum at the location corresponding to individual i to cum_sum+fitness
		cur_fit = fitnesses[i]
		if cur_fit < 0:
			# we don't allow for negative fitness in practice, instead setting its selection probability to zero
			cur_fit = 0
		cum_sum += cur_fit
		cum_fitnesses[i] = cum_sum
	
	for i in range(num_samples):
		rand_index = random()*cum_sum
		# for each new parent, select a parent p with probability fitness(p)/total fitnesses
		samples[i] = population[binarySearch(cum_fitnesses, rand_index)]
	return samples

def geneticGerrymander(state: State, num_districts, pop_size, combination_proportion, generations, recombinations,sampling_strategy=fitness_proportional_sampling, favored=1):
	# we assume that "state" is uninitialized
	"""
	inputs:
	state - the state object to be gerrymandered
	num_districts - the number of districts into which the state will be divided
	pop_size - the number of maps tracked in each iteration
	combination_proportion - the portion of districts which are taken from the parents
	generations - lcv. the number of generations to simulate
	sampling_strategy - a function which chooses parents for subsequent generations from a population
	favored - the party we are trying to artificially support
	
	
	output:
	state - gerrymandered state
	
	# TODO: make cleaner and easier to use
	* maybe a factory?
	* definitely abstract parts out
	"""
	
	population = [0]*pop_size # initialize a list to track the population
	init_map = resetMatrix(cloneMatrix(state.voting_outcome)) # create a new copy of the voting outcome which will be the district matrix
	# resetMatrix sets all values to -1
	for i in range(pop_size):
		new_map = fmap(init_map, num_districts, 0) # make a random map
		new_state = state.clone()
		new_state.instantiate(new_map) # create a new copy of the state with the new map
		population[i] = new_state      # store the new state/map in the popuplation
	# at this point, we have generated the initial population	
	
	generation = 0 # define the lcv
	while generation < generations:
		# choose two parents per offspring with constant population size = 2*pop_size
		samples = sampling_strategy(population, 2*pop_size, favored=favored)
		for i in range(pop_size):
			s1 = samples[int(random()*len(samples)/2)] # choose 2 random parents from the sample
			s2 = samples[int(random()*len(samples)/2)]
			child = reproduce(s1, s2, combination_proportion)
			while not child: # keep trying with new parents until they are compatible
				s1 = samples[int(random()*len(samples)/2)]
				s2 = samples[int(random()*len(samples)/2)]
				child = reproduce(s1, s2, combination_proportion)
			population[i] = child # store the output child
	
		# recombination - UNTESTED
		# @Robert don't bother looking through this loop yet, I don't remember how it works
		# but will check, clean, comment, fix if necessary
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
						if districtIsSeparated(s.district_matrix, growing_dist):
							# district was separated, so we need to revert the change
							growing_dist = growing_dist[0:len(growing_dist)-1]
							shrinking_dist.append(n)
						else: 
							changed = True
				if not changed:
					lcv += 1
		generation += 1
	# we have now concluded simulation	
	
	index = 0
	max_fitness = -1
	for i in range(pop_size):
		f = compute_fitness(favored, population[i])
		if f > max_fitness:
			max_fitness = f
			index = i
	return population[index]
	
def neighborhoodGerrymander(state: State, num_districts, pop_size, distance, iterations, favored=1):
	"""
	inputs:
	state - the state object to be gerrymandered
	favored - the party we are trying to artificially support
	pop_size - the number of maps tracked in each iteration
	num_districts - the number of districts into which the state will be divided
	iterations - the number of times to loop
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
	
def reproduce(state1: State, state2: State, combination_proportion):
	"""
	inputs:
	state1, state2 - parent State objects
	combination_proportion - the desired threshold to combine from parents before finishing maps randomly
	
	
	# TODO: generalize
	* allow for slightly overlapping districts, i.e. add parameter permissible_overlap
	"""
	district_matrix = resetMatrix(cloneMatrix(state1.voting_outcome)) # get matrix of all -1s w/ appropriate dimensions
	num_districts = len(state1.districts) # the two districts should have the same number of districts
	num_precincts = sum(len(state1.district_matrix[i]) for i in range(len(state1.district_matrix)))
	district_candidates = [0]*2*num_districts # candidate districts to appear in the child
	for i in range(num_districts):
		# we store district candidates as tuples so that there state IDs can also be included
		# parents could also be computed via modular arithmetic, but I didn't, so there.
		# either option allows for generalized reproduction (n-parent)
		district_candidates[i] = (1, i)
		district_candidates[num_districts+i] = (2, i)
	# we have finished set-up for the interesting part
	
	# track the numbers of decisions that have already been made
	precincts_assigned = 0
	districts_assigned = 0
	
	# we continue until we have "enough" precincts assigned via this method
	while precincts_assigned < combination_proportion*num_precincts and len(district_candidates) > 0 and districts_assigned < num_districts:
		index = int(random()*len(district_candidates)) # choose a random district
		temp = district_candidates[index]
		state_ID = temp[0]
		district_ID = temp[1]
		del district_candidates[index] # remove the district as an option
		if state_ID == 1: # identify the parent state
			state = state1
		else:
			state = state2
		no_intersection = True
		
		# ensure no precinct in the new district belongs to an existing 
		for p in state.getDistrictByID(district_ID).precincts:
			if district_matrix[p[0]][p[1]] != -1:
				no_intersection = False
				break
		
		if no_intersection:
			# assuming we have sufficiently small overlap, instantiate the new district
			for p in state.getDistrictByID(district_ID).precincts:
				district_matrix[p[0]][p[1]] = districts_assigned
			districts_assigned += 1
			precincts_assigned += len(state.getDistrictByID(district_ID).precincts)
			
	# finish off the new map randomly, clone the state, and return a state object with the new map
	district_matrix = fmap(district_matrix, num_districts, districts_assigned)
	child = state1.clone()
	child.instantiate(district_matrix)
	return child


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
		
	
def fmap(matr, num_districts, districts_assigned):
	matr = cloneMatrix(matr)
	remaining_districts = num_districts - districts_assigned
	for i in range(remaining_districts):
		district_start = (-1,-1)
		while not is_unmatched(district_start, matr):
			x = int(random()*len(matr))
			y = int(random()*len(matr[x]))
			district_start = (x,y)
		matr[district_start[0]][district_start[1]] = districts_assigned
		districts_assigned += 1
	
	candidates = []
	for i in range(len(matr)):
		for j in range(len(matr[i])):
			if is_matched((i,j), matr):
				neighbors = ((i-1,j),(i,j-1),(i+1,j),(i,j+1))
				for n in neighbors:
					if is_unmatched(n, matr) and not n in candidates:
						candidates.append(n)
	
	while candidates != []:
		candidate_index = int(random()*len(candidates))
		precinct = candidates[candidate_index]
		x = precinct[0]; y = precinct[1]
		neighbors = [(x-1,y),(x,y-1),(x+1,y),(x,y+1)]
		district_options = []
		for n in neighbors:
			if is_matched(n, matr):
				if not matr[n[0]][n[1]] in district_options:
					district_options.append(matr[n[0]][n[1]])
			elif is_unmatched(n, matr) and not n in candidates:
				candidates.append(n)
		chosen_option = district_options[int(random()*len(district_options))]
		matr[x][y] = chosen_option
		del candidates[candidate_index]
	return matr


def update_district_matrix(district_matrix, district_list, district_ID):
	"""
	helper - set of district_matrix, given by district_list, to the value district_ID
	"""
	for pos in district_list:
		x = pos[0]; y = pos[1]
		district_matrix[x][y] = district_ID
	

def is_unmatched(ordered_pair, district_matrix):
	"""
	helper - return True if the location described by ordered pair has -1,
					False if the location is out of scope or has anything else
	"""
	x = ordered_pair[0]; y = ordered_pair[1]
	if x<0 or y<0 or x>=len(district_matrix) or y>=len(district_matrix[x]):
		return False
	return district_matrix[x][y] == -1
	

def is_matched(ordered_pair, district_matrix):
	"""
	helper - return True if the location described by ordered pair has anything other than -1
					False if the location is out of scope or has -1
	"""
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
	"""
	helper - repeatedly 
	"""
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
	"""
	helper - perform a breadth first search to find a continuous group of precincts 
			which meet some criterion specified by fun
	inputs:
	start - location of beginning of breadth-first search
	fun - function specifying criterion, takes in an ordered pair and the matrix
	matr - the map on which to conduct the search
	
	output:
	group - a list of ordered pairs which were found by the search
	"""
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
	"""
	given a list and a value, search for the index that has the first value larger the one supplied
	cum_fitnesses - list of cumulative fitnesses to be searched
		* because cumulative fitnesses are listed, the values are ascending
	rand_value - the search value
	"""
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
	"""
	helper - set every numeric value in a (2D) array to -1
	"""
	for i in range(len(matr)):
		for j in range(len(matr[i])):
			matr[i][j] = -1
	return matr