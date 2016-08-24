import fileinput

def parseIplInst( files ):
	class INSTline:
		def __init__(self):
			self.ModelID = -1
			self.ModelName = ""
			self.Interior = 0
			self.Pos = ()
			self.Scale = ()
			self.Rot = ()

	parse = False
	instlist = {}
	for line in fileinput.input( files ):
		line = line.strip()
		if line.startswith('#'):
			continue
		if line == "end":
			parse = False

		if parse == True:
			tokens = line.split(", ")
			modelId = int(tokens[0])
			instlist.setdefault( modelId, [])

			inst = INSTline()
			inst.ModelID = modelId
			inst.ModelName = tokens[1]
			if len(tokens) == 12:
				inst.Pos = ( float(tokens[2]), float(tokens[3]), float(tokens[4]) )
				inst.Scale = ( float(tokens[5]), float(tokens[6]), float(tokens[7]) )
				inst.Rot = ( float(tokens[8]), float(tokens[9]), float(tokens[10]), float(tokens[11]) )
			elif len(tokens) == 13:
				inst.Pos = ( float(tokens[3]), float(tokens[4]), float(tokens[5]) )
				inst.Interior = int(tokens[2])
				inst.Scale = ( float(tokens[6]), float(tokens[7]), float(tokens[8]) )
				inst.Rot = ( float(tokens[9]), float(tokens[10]), float(tokens[11]), float(tokens[12]) )
			instlist[ modelId ].append( inst )

		if line == "inst":
			parse = True

	return instlist