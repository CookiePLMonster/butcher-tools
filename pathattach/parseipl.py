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
		line = line.strip().split('#', 1)[0]
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

def parseIplPath( files ):
	# We store IDE paths in a dictionary with modelID key, but IPL paths should be stored
	# in a plain list
	class PATHnode:
		def __init__(self):
			self.NodeType = 0
			self.NextNode = -1
			self.IsCrossRoad = False
			self.Pos = ()
			self.Median = 0.0
			self.LeftLanes = -1
			self.RightLanes = -1
			self.SpeedLimit = -1
			self.Flags = -1
			self.SpawnRate = 0.0

	class PATHgroup:
		def __init__(self):
			self.GroupID = -1
			self.ModelID = -1
			self.Nodes = []

		def __init__(self, group, id):
			self.GroupID = group
			self.ModelID = id
			self.Nodes = []

	parse = False
	pathlist = []
	for line in fileinput.input( files ):
		line = line.strip().split('#', 1)[0]
		if line == "end":
			parse = False

		if parse == True:
			tokens = line.split(", ")
			if len(tokens) == 2:
				curGroup = int(tokens[0])
				curModel = int(tokens[1])
				pathlist.append( PATHgroup( curGroup, curModel ) )
			elif len(tokens) == 12:
				node = PATHnode()
				node.NodeType = int(tokens[0])
				node.NextNode = int(tokens[1])
				node.IsCrossRoad = int(tokens[2])
				node.Pos = ( float(tokens[3]), float(tokens[4]), float(tokens[5]) )
				node.Median = float(tokens[6])
				node.LeftLanes = int(tokens[7])
				node.RightLanes = int(tokens[8])
				node.SpeedLimit = int(tokens[9])
				node.Flags = int(tokens[10])
				node.SpawnRate = float(tokens[11])

				pathlist[ -1 ].Nodes.append( node )

		if line == "path":
			parse = True

	return pathlist