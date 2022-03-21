from utilities.readState import *
from utilities import metrics

rowStateDistricts, rowStateVotes = readState("states/state1")
colStateDistricts, colStateVotes = readState("states/state2")

#######################################################
# compactness tests
#######################################################
"""
for all districts:
	compute center most (try all (precinct, precinct) pairs)
	for all precincts:
		add max(height diff/width diff)^2
"""
def compactnessTestRowState():
	metrics.setState(rowStateDistricts, rowStateVotes)
	assert metrics.compactness() == 5**2 + 2*(4**2 + 3**2 + 2**2 + 1)

def compactnessTestColState():
	metrics.setState(colStateDistricts, colStateVotes)
	assert metrics.compactness() == 5**2 + 2*(4**2 + 3**2 + 2**2 + 1)


#######################################################
# elongatedness tests
#######################################################
def elongatednessTestRowState():
	pass
	
def elongatednessTestRowState():
	pass

#######################################################
# indentedness tests
#######################################################
def indentednessTestRowState():
	pass
	
def indentednessTestColState():
	pass

#######################################################
# puncture tests
#######################################################
def puncturedTestRowState():
	pass
	
def puncturedTestColState():
	pass

#######################################################
# separation tests
#######################################################
def separationTestRowState():
	pass
	
def separationTestColState():
	pass