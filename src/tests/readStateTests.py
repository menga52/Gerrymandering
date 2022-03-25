from utilities.readState import *

def testRowState():
	districts, votes = readState("states/state1")
	
	cDistricts = [];
	cVotes = [];
	for i in range(10):
		rowD = []
		rowV = []
		for j in range(10):
			rowD.append(i)
			rowV.append(1)
		cDistricts.append(rowD)
		cVotes.append(rowV)
	
	assert districts == cDistricts
	assert votes == cVotes
	
def testColState():
	districts, votes = readState("states/state2")
	
	cDistricts = [];
	cVotes = [];
	for i in range(10):
		rowD = []
		rowV = []
		for j in range(10):
			rowD.append(j)
			rowV.append(1)
		cDistricts.append(rowD)
		cVotes.append(rowV)
	
	assert districts == cDistricts
	assert votes == cVotes
	
def testVotingOutcomeUnfair():
	votes = readStateWithoutDistricts("states/votingOutcome1")
	
	cVotes = [];
	for i in range(10):
		rowV = []
		for j in range(10):
			rowV.append(1)
		cVotes.append(rowV)
	
	assert votes == cVotes