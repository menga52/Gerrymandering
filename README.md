# Gerrymandering
<p>
  This repository will house the documentation pertaining to an independent study exploring mathematical approaches to district gerrymandering and recognition of gerrymandering.
</p>
<h2>Use cases</h2>
<h4>Setup</h4>
Run:
pip install .
from utilities.readState import readStateWithoutDistricts as read
[state] = read('states/[filename]')
<hr>

<h4>Run a genetic gerrymander with a districts, b individuals per population, c (in [0,1]) combination proportion, d generations, and e recombinations</h4>
from utilities.gerrymander import *
[output] = geneticGerrymander(state, 20, 10, 0.4. 10, 0)
<hr>

<h4>Display a map</h4>
from utilities.utilities import *
displayMap(output.district_matrix)

<h2>Dependencies</h2>
pip install structlinks
<h2>Directory structure</h2>
<h3>src</h3>
Source code
<h4>states</h4>
.txt files defining vote outcomes of "states"
<h4>tests</h4>
tests of basic functionality
<h4>utilities</h4>
basic functionality
<h3>TODO</h3>
Test genetic algorithm
comment uncommented functions
refactor names
all the TODOs in the code
abstract recombination stage into function
write a parameters object

<h3>Notes</h3>
The genetic algorithm works in theory, but the others used random swaps and resulted in disconnected maps.
Solution: a function which checks whether a precinct is a cut vertex before swapping it
Problem: infinite loop somewhere, exceptionally unclear where
