import fileinput

def parseIpl( files ):
	parse = False
	inst = {}
	for line in fileinput.input( files ):
		line = line.strip()
		if line.startswith('#'):
			continue
		if line == "end":
			parse = False

		if parse == True:
			tokens = line.split(", ")
			inst.setdefault( tokens[0], [])
			if len(tokens) == 12:
				inst[ tokens[0] ].append( (tokens[1], float(tokens[2]), float(tokens[3]), float(tokens[4]), float(tokens[8]), float(tokens[9]), float(tokens[10]), float(tokens[11])) )
			elif len(tokens) == 13:
				inst[ tokens[0] ].append( (tokens[1], float(tokens[3]), float(tokens[4]), float(tokens[5]), float(tokens[9]), float(tokens[10]), float(tokens[11]), float(tokens[12])) )

		if line == "inst":
			parse = True

	return inst