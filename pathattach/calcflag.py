import sys
if len(sys.argv) != 4:
	print 'calcflag usage:'
	print 'python calcflag.py [orig_flag] [modelID] [instanceID]'
	quit()

flag = int(sys.argv[1])
id = int(sys.argv[2])
instId = int(sys.argv[3])

OutFlag = (flag & 0xF) | ((id & 0xFFFF) << 4) | ((instId & 0xFFF) << 20)
OutFlag &= 0xFFFFFFFF
print 'Required flag is ' + str(OutFlag)