import sys
import fileinput
import numpy as np

parse = False
instlines = {}
for line in fileinput.input(sys.argv[2:]):
	line = line.strip()
	if line.startswith('#'):
		continue
	if line == "end":
		parse = False

	if parse == True:
		tokens = line.split(", ")
		if tokens[0] not in instlines:
			if len(tokens) == 12:
				instlines.update( {tokens[0] : ( tokens[1], tokens[2], tokens[3], tokens[4], tokens[8], tokens[9], tokens[10], tokens[11] ) })
			elif len(tokens) == 13:
				instlines.update( {tokens[0] : ( tokens[1], tokens[3], tokens[4], tokens[5], tokens[9], tokens[10], tokens[11], tokens[12] ) })

	if line == "inst":
		parse = True

curData = ()
parse = False
parseThisFile = False
with open(sys.argv[1]) as f:
	for line in f:
		line = line.strip()
		if line.startswith('#'):
			continue
		if line == "end":
			parse = False

		if parse == True:
			tokens = line.split(", ")
			if len(tokens) == 3:
				if tokens[1] in instlines:
					curData = instlines[ tokens[1] ]
					parseThisFile = True
					print tokens[0] + ', -1, ' + tokens[1]
				else:
					print >> sys.stderr, "Error! File " + tokens[2] + " not found in any parsed IPL!"
					parseThisFile = False
			elif len(tokens) == 12 and parseThisFile == True:
				if tokens[0] == '0':
					print '\t0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1'
				else:
					v = [ float(tokens[3]), float(tokens[4]), float(tokens[5]) ]
					u = [ -float(curData[4]), -float(curData[5]), -float(curData[6]) ]
					s = float(curData[7])
					vprime = 2.0 * np.dot(u, v) * u + (s*s - np.dot(u, u)) * v + 2.0 * s * np.cross(u, v)
					vprime += [ float(curData[1]) * 16.0, float(curData[2]) * 16.0, float(curData[3]) * 16.0 ]
					print '\t' + tokens[0] + ', ' + tokens[1] + ', ' + tokens[2] + ', ' + str(vprime[0])  + ', ' + str(vprime[1]) + ', ' + str(vprime[2]) + ', ' + tokens[6] + ', ' + tokens[7] + ', ' + tokens[8] + ', ' + tokens[9] + ', ' + tokens[10] + ', ' + tokens[11]

		if line == "path":
			parse = True