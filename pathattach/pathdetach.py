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


instlines = parseIplInst( sys.argv[2:] )
paths = parseIdePath( sys.argv[1] )

for id, path in paths.iteritems():
	if id not in instlines:
		print >> sys.stderr, "Error! File " + path.ModelName + " not found in any parsed IPL!"
		continue

	for groupId, pathnodes in enumerate(path.NodesByGroup):
		if pathnodes:
			for inst in instlines[ path.ModelID ]:
				print str(groupId) + ', -1 # ' + str(id) + ', ' + path.ModelName
				for node in pathnodes:
					NewPos = ()
					if node.NodeType == 0:
						NewPos = (0, 0, 0)
					else:
						q = ( inst.Rot[3], -inst.Rot[0], -inst.Rot[1], -inst.Rot[2] )
						qc = wxyzConjugate(q)
						p = ( 0.0, ) + node.Pos

						v = quatMultiply(quatMultiply(q, p), qc)
						NewPos = map(lambda x, y: int(x + y*16.0), v[1:], inst.Pos)
					print '\t' + str(node.NodeType) + ', ' + str(node.NextNode) + ', ' + str(node.IsCrossRoad) + ', ' + \
					str(NewPos[0]) + ', ' + str(NewPos[1])  + ', ' + str(NewPos[2]) + ', ' + \
					str(node.Median) + ', ' + str(node.LeftLanes) + ', ' + str(node.RightLanes) + ', ' + \
					str(node.SpeedLimit) + ', ' + str(node.Flags) + ', ' + str(node.SpawnRate)