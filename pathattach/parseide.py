import fileinput

def parseIdePath( files ):
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
			self.ModelID = -1
			self.ModelName = ""
			self.NodesByGroup = [], [], []

		def __init__(self, id, name):
			self.ModelID = id
			self.ModelName = name
			self.NodesByGroup = [], [], []

	parse = False
	pathlist = {}
	curModel = -1
	curGroup = -1
	for line in fileinput.input( files ):
		line = line.strip()
		if line.startswith('#'):
			continue
		if line == "end":
			parse = False

		if parse == True:
			tokens = line.split(", ")
			if len(tokens) == 3:
				curGroup = int(tokens[0])
				curModel = int(tokens[1])
				pathlist.setdefault( curModel, PATHgroup( curModel, tokens[2] ) )
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

				pathlist[ curModel ].NodesByGroup[ curGroup ].append( node )

		if line == "path":
			parse = True

	return pathlist