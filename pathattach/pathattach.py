import sys
import copy
from parseipl import parseIplInst
from parseipl import parseIplPath

def wxyzConjugate(q):
	return q[0], -q[1], -q[2], -q[3]

def quatMultiply(q, p):
	return q[0]*p[0] - q[1]*p[1] - q[2]*p[2] - q[3]*p[3], \
	q[0]*p[1] + q[1]*p[0] + q[2]*p[3] - q[3]*p[2], \
	q[0]*p[2] + q[2]*p[0] + q[3]*p[1] - q[1]*p[3], \
	q[0]*p[3] + q[3]*p[0] + q[1]*p[2] - q[2]*p[1]

firstArg = 1
Verbose = False
IncludeSection = False

for arg in sys.argv[1:]:
	if arg == '-verbose':
		Verbose = True
		firstArg += 1
	elif arg == '-mksection':
		IncludeSection = True
		firstArg += 1
	else:
		break

instlines = parseIplInst( sys.argv[firstArg+1:] )
paths = parseIplPath( sys.argv[firstArg] )

processed = set()

if IncludeSection:
	print 'path'

for id, path in enumerate(paths):
	if path.Nodes:
		# Find the model this path group originates from
		Flag = path.Nodes[0].Flags
		OrigFlags = Flag & 0xF;
		OrigModel = (Flag >> 4) & 0xFFFF
		OrigInsID = (Flag >> 20) & 0xFFF
		if OrigModel == 0:
			print >> sys.stderr, 'Path ' + str(id) + ' has no modelID assigned, skipping'
			continue
		if OrigModel in instlines:
			inst = instlines[ OrigModel ][ OrigInsID ]
			if (OrigModel, path.GroupID) in processed:
				if Verbose:
					print >> sys.stderr, 'Path for model ' + inst.ModelName + ' already processed, skipping'
				continue
			processed.add( (OrigModel, path.GroupID) )

			print str(path.GroupID)  + '. ' + str(OrigModel) + ', ' + inst.ModelName
			for node in path.Nodes:
				NewPos = ()
				if node.NodeType == 0:
					NewPos = (0, 0, 0)
				else:
					v = map(lambda x, y: y - x*16.0, inst.Pos, node.Pos)
					q = ( inst.Rot[3], ) + tuple(inst.Rot[:3])
					qc = wxyzConjugate(q)
					p = ( 0.0, ) + tuple(v)

					NewPos = v
				print '\t' + str(node.NodeType) + ', ' + str(node.NextNode) + ', ' + str(node.IsCrossRoad) + ', ' + \
				"{:g}".format(NewPos[0]) + ', ' + "{:g}".format(NewPos[1])  + ', ' + "{:g}".format(NewPos[2]) + ', ' + \
				"{:g}".format(node.Median) + ', ' + str(node.LeftLanes) + ', ' + str(node.RightLanes) + ', ' + \
				str(node.SpeedLimit) + ', ' + str(OrigFlags) + ', ' + "{:g}".format(node.SpawnRate)

if IncludeSection:
	print 'end'