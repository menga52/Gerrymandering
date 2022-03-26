from utilities.readState import readState as read
from utilities.metrics import *

d, v = read("states/punctureExample1")
p = findDistricts(d)
numPunctures(0, p, d)