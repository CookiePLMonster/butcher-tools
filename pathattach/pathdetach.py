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
		if len(tokens) == 12:
			instlines.setdefault( tokens[0], []).append( ( tokens[1], float(tokens[2]), float(tokens[3]), float(tokens[4]), float(tokens[8]), float(tokens[9]), float(tokens[10]), float(tokens[11]) ) )
		elif len(tokens) == 13:
			instlines.setdefault( tokens[0], []).append( ( tokens[1], float(tokens[3]), float(tokens[4]), float(tokens[5]), float(tokens[9]), float(tokens[10]), float(tokens[11]), float(tokens[12]) ) )

	if line == "inst":
		parse = True

with open(sys.argv[1]) as f:
	parse = False
	parseThisFile = False
	curIde = []
	curIdeType = 0
	curIdeModel = 0

	for line in f:
		line = line.strip()
		if line.startswith('#'):
			continue
		if line == "end":
			parse = False

		if parse == True:
			tokens = line.split(", ")
			if len(tokens) == 3:
				# If has anything, serialize
				if len(curIde) > 0:
						if curIdeModel in instlines:
							for curData in instlines[ curIdeModel ]:
								print curIdeType + ', -1, ' + curIdeModel
								for token in curIde:
									if curIde[0] == '0':
										print '\t0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1'
									else:
										q = [ curData[7], curData[4], curData[5], curData[6] ]
										qc = [ curData[7], -curData[4], -curData[5], -curData[6] ]
										p = [ 0.0, float(token[3]), float(token[4]), float(token[5]) ]

										vprime = [ q[0]*p[0] - q[1]*p[1] - q[2]*p[2] - q[3]*p[3], \
										q[0]*p[1] + q[1]*p[0] + q[2]*p[3] - q[3]*p[2], \
										q[0]*p[2] + q[2]*p[0] + q[3]*p[1] - q[1]*p[3], \
										q[0]*p[3] + q[3]*p[0] + q[1]*p[2] - q[2]*p[1] ]

										vprime = [ vprime[0]*qc[0] - vprime[1]*qc[1] - vprime[2]*qc[2] - vprime[3]*qc[3], \
										vprime[0]*qc[1] + vprime[1]*qc[0] + vprime[2]*qc[3] - vprime[3]*qc[2], \
										vprime[0]*qc[2] + vprime[2]*qc[0] + vprime[3]*qc[1] - vprime[1]*qc[3], \
										vprime[0]*qc[3] + vprime[3]*qc[0] + vprime[1]*qc[2] - vprime[2]*qc[1] ]

										print '\t' + token[0] + ', ' + token[1] + ', ' + token[2] + ', ' + str(vprime[1] + curData[1] * 16.0)  + ', ' + str(vprime[2] + curData[2] * 16.0) + ', ' + str(vprime[3] + curData[3] * 16.0) + ', ' + token[6] + ', ' + token[7] + ', ' + token[8] + ', ' + token[9] + ', ' + token[10] + ', ' + token[11]
				curIde = []


				if tokens[1] in instlines:
					#curData = instlines[ tokens[1] ]
					parseThisFile = True
					curIdeType = tokens[0]
					curIdeModel = tokens[1]
				else:
					print >> sys.stderr, "Error! File " + tokens[2] + " not found in any parsed IPL!"
					parseThisFile = False
			elif len(tokens) == 12 and parseThisFile == True:
				curIde.append( tokens )

		if line == "path":
			parse = True