from utilities.gerrymander import *
from utilities.readState import readStateWithoutDistricts as read
from utilities.metrics import *

#TODO: adjust tests to call gerrymandering algo with strategy pattern

def testGerrymanderUnfairGenetic():
	votingOutcome = read("states/votingOutcome1")
	districts = geneticGerrymander(votingOutcome)
	sums = computeVotesEqualWeight(districts)
	assert sums[0] > 0 and sums[1] == 0
	
def testGerrymanderUnfairNearestNeighbor():
	votingOutcome = read("states/votingOutcome1")
	districts = nearestNeighborGerrymander(votingOutcome)
	sums = computeVotesEqualWeight(districts)
	assert sums[0] > 0 and sums[1] == 0
	
def testAlternatingRowVotingOutcomeGenetic():
	votingOutcome = read("states/alternatingRowVotingOutcome")
	districts = geneticGerrymander(votingOutcome)
	sums = computeVotesEqualWeight(districts)
	assert sums[1] > sums[0]
	
def testAlternatingRowVotingOutcomeNearestNeighbor():
	votingOutcome = read("states/alternatingRowVotingOutcome")
	districts = nearestNeighborGerrymander(votingOutcome)
	sums = computeVotesEqualWeight(districts)
	assert sums[1] > sums[0]
	
def testBisectionVotingOutcomeGenetic():
	votingOutcome = read("states/bisectionVotingOutcome")
	districts = geneticGerrymander(votingOutcome)
	sums = computeVotesEqualWeight(districts)
	assert sums[1] > sums[0]
	
def testBisectionVotingOutcomeNearestNeighbor():
	votingOutcome = read("states/bisectionVotingOutcome")
	districts = nearestNeighborGerrymander(votingOutcome)
	sums = computeVotesEqualWeight(districts)
	assert sums[1] > sums[0]
	
def testGridVotingOutcomeGenetic():
	votingOutcome = read("states/gridVotingOutcome")
	districts = geneticGerrymander(votingOutcome)
	sums = computeVotesEqualWeight(districts)
	assert sums[1] > sums[0]
	
def testGridVotingOutcomeNearestNeighbor():
	votingOutcome = read("states/gridVotingOutcome")
	districts = nearestNeighborGerrymander(votingOutcome)
	sums = computeVotesEqualWeight(districts)
	assert sums[1] > sums[0]
