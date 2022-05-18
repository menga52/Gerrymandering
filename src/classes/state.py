import sys


class District:
	"""
	This class represents a district in an instantiated map of a state.
	
	precincts - a list of precincts which belong to a district
	minX - the x-index of a leftmost precinct in the district
	maxX - the x-index of a rightmost precinct in the district
	minY - the y-index of a topmost precinct in the district
	maxY - the y-index of a bottommost precinct in the district
	"""
	precincts = None
	minX = None
	maxX = None
	minY = None
	maxY = None
	id = None
	
	def findExtremes(self):
		"""
		This function computes minX, maxX, minY, and maxY given a list of precincts
		"""
		self.minX = sys.maxsize
		self.maxX = -1
		self.minY = sys.maxsize
		self.maxY = -1
		for (x, y) in self.precincts:
			if x < self.minX: self.minX = x
			if y < self.minY: self.minY = y
			if x > self.maxX: self.maxX = x
			if y > self.maxY: self.maxY = y
	
	
	def __init__(self, id, precinct_list):
		self.precincts = precinct_list
		self.id = id
		self.findExtremes()
		
class State:
	"""
	This class represents a state or region which is to be analyzed or gerrymandered.
	
	instantiated - whether state has districts associated with it
	district_matrix - a two-dimensional array of the state where (i,j)=k means precinct (i,j) is in district k
	voting_outcome - a two-dimensional array of the state where (i,j)=k means precinct (i,j) votes for candidate k
	districts - a list of District objects that define the state. 
	"""
	instantiated = False
	district_matrix = None  
	voting_outcome = None
	districts = None
	
	# TODO: add memoization of district-level metrics
	
	def __init__(self, voting_outcome, district_matrix=None):
		self.voting_outcome = voting_outcome
		if district_matrix != None:
			self.district_matrix = district_matrix
			self.instantiated = True
			district_dict = findDistricts(district_matrix)
			self.districts = []
			for district_id in district_dict:
				self.districts.append(District(district_id, district_dict[district_id]))
				
				
	def instantiate(self, district_matrix):
		"""
		add a district map to the state
		inputs: 
		district_matrix - a two-dimensional representation of the districts
		
		outputs:
		mutates the state object to be instantiated and have districts
		"""
		self.district_matrix = district_matrix
		self.instantiated = True
		district_dict = findDistricts(district_matrix)
		self.districts = []
		for district_id in district_dict:
			self.districts.append(District(district_id, district_dict[district_id]))
				
	def clone(self):
		new_voting_outcome = cloneMatrix(self.voting_outcome)
		return State(new_voting_outcome, self.district_matrix)
	
	def cloneInstantiated(self):
		new_voting_outcome = cloneMatrix(self.voting_outcome)
		new_district_matrix = cloneMatrix(self.district_matrix)
		return State(new_voting_outcome, new_district_matrix)
		
	def getDistrictNumber(self, x, y):
		if x < 0 or x >= len(self.district_matrix) or y < 0 or y >= len(self.district_matrix[x]):
			return -1
		return self.district_matrix[x][y]
		
	def getDistrictByID(self, district_ID):
		for d in self.districts:
			if d.id == district_ID:
				return d
		return None
		
		
	
def cloneMatrix(matr):
	out = [0]*len(matr)
	for i in range(len(out)):
		out[i] = [0]*len(matr[i])
		for j in range(len(matr[i])):
			out[i][j] = matr[i][j]
	return out
				

def findDistricts(district_matrix):
	"""
	This function searches through a state to identify which precincts belong to which district
	inputs:
	districts - a two-dimensional array of district numbers where districts[i][j] = k means (i, j) is in district k
	
	outputs:
	precincts - a dictionary whose keys districts and whose values are lists of coordianates
	"""
	precincts = {}
	for i in range(len(district_matrix)):
		for j in range(len(district_matrix[i])):
			if district_matrix[i][j] not in precincts:
				precincts[district_matrix[i][j]] = []
			precincts[district_matrix[i][j]].append((i, j))
	return precincts