import sys
import copy
from parseipl import parseIplInst
from parseide import parseIdePath

def wxyzConjugate(q):
	return q[0], -q[1], -q[2], -q[3]

def quatMultiply(q, p):
	return q[0]*p[0] - q[1]*p[1] - q[2]*p[2] - q[3]*p[3], \
	q[0]*p[1] + q[1]*p[0] + q[2]*p[3] - q[3]*p[2], \
	q[0]*p[2] + q[2]*p[0] + q[3]*p[1] - q[1]*p[3], \
	q[0]*p[3] + q[3]*p[0] + q[1]*p[2] - q[2]*p[1]

firstArg = 1
StripDebugInfo = False
IncludeIDEInfo = False
IncludeSection = False

for arg in sys.argv[1:]:
	if arg == '-nodebug':
		StripDebugInfo = True
		firstArg += 1
	elif arg == '-ideinfo':
		IncludeIDEInfo = True
		firstArg += 1
	elif arg == '-mksection':
		IncludeSection = True
		firstArg += 1
	else:
		break

instlines = parseIplInst( sys.argv[firstArg+1:] )
paths = parseIdePath( sys.argv[firstArg] )

if IncludeSection:
	print 'path'

for id, path in paths.iteritems():
	if id not in instlines:
		print >> sys.stderr, "Error! File " + path.ModelName + " not found in any parsed IPL!"
		continue

	for groupId, pathnodes in reversed(list(enumerate(path.NodesByGroup))):
		if pathnodes:
			for instId, inst in enumerate(instlines[ path.ModelID ]):
				if StripDebugInfo:
					print str(groupId) + ', -1 # ' + str(id) + ', ' + path.ModelName
				else:
					print str(groupId) + ', -1'
				for nodeId, node in enumerate(pathnodes):
					NewFlags = node.Flags
					if IncludeIDEInfo and nodeId == 0:
						NewFlags &= 0xF
						NewFlags |= (id & 0xFFFF) << 4
						NewFlags |= (instId & 0xFFF) << 20

					NewPos = ()
					if node.NodeType == 0:
						NewPos = (0, 0, 0)
					else:
						q = ( inst.Rot[3], ) + tuple(inst.Rot[:3])
						qc = wxyzConjugate(q)
						p = ( 0.0, ) + node.Pos

						v = quatMultiply(quatMultiply(q, p), qc)
						NewPos = map(lambda x, y: x + y*16.0, v[1:], inst.Pos)
					print '\t' + str(node.NodeType) + ', ' + str(node.NextNode) + ', ' + str(node.IsCrossRoad) + ', ' + \
					"{:g}".format(NewPos[0]) + ', ' + "{:g}".format(NewPos[1])  + ', ' + "{:g}".format(NewPos[2]) + ', ' + \
					"{:g}".format(node.Median) + ', ' + str(node.LeftLanes) + ', ' + str(node.RightLanes) + ', ' + \
					str(node.SpeedLimit) + ', ' + str(NewFlags) + ', ' + "{:g}".format(node.SpawnRate)

if IncludeSection:
	print 'end'