import sys
from parseipl import parseIplInst

def wxyzConjugate(q):
	return q[0], -q[1], -q[2], -q[3]

def quatMultiply(q, p):
	return q[0]*p[0] - q[1]*p[1] - q[2]*p[2] - q[3]*p[3], \
	q[0]*p[1] + q[1]*p[0] + q[2]*p[3] - q[3]*p[2], \
	q[0]*p[2] + q[2]*p[0] + q[3]*p[1] - q[1]*p[3], \
	q[0]*p[3] + q[3]*p[0] + q[1]*p[2] - q[2]*p[1]


with open(sys.argv[1]) as f:
	parse = False
	parseThisFile = False
	curIde = []
	curIdeType = 0
	curIdeModel = 0
	curIdeName = ""

	instlines = parseIplInst( sys.argv[2:] )

	for line in f:
		line = line.strip()
		if line.startswith('#'):
			continue
		if line == "end":
			parse = False

		if parse == True:
			tokens = line.split(", ")
			if len(tokens) == 3:
				if curIde:
					for inst in instlines[ curIdeModel ]:
						print str(curIdeType) + ', -1 # ' + str(curIdeModel) + ', ' + curIdeName
						for token in curIde:
							out = ()
							if int(token[0]) == 0:
								out = (0, 0, 0)
							else:
								q = ( inst.Rot[3], -inst.Rot[0], -inst.Rot[1], -inst.Rot[2] )
								qc = wxyzConjugate(q)
								p = [ 0.0, float(token[3]), float(token[4]), float(token[5]) ]

								v = quatMultiply(quatMultiply(q, p), qc)
								out = map(lambda x, y: int(x + y*16.0), v[1:], inst.Pos)

							print '\t' + token[0] + ', ' + token[1] + ', ' + token[2] + ', ' + str(out[0])  + ', ' + str(out[1]) + ', ' + str(out[2]) + ', ' + token[6] + ', ' + token[7] + ', ' + token[8] + ', ' + token[9] + ', ' + token[10] + ', ' + token[11]

				curIde = []
				modelId = int(tokens[1])
				if modelId in instlines:
					parseThisFile = True
					curIdeType = int(tokens[0])
					curIdeModel = modelId
					curIdeName = tokens[2]
				else:
					print >> sys.stderr, "Error! File " + tokens[2] + " not found in any parsed IPL!"
					parseThisFile = False
			elif len(tokens) == 12 and parseThisFile == True:
				curIde.append( tokens )

		if line == "path":
			parse = True