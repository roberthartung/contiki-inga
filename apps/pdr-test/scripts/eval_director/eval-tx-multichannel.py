#!/usr/bin/python
import time
import testbedclient

seqnrfile = '/tmp/tmp/pn-seqnr'
broadcastdest = 65535

idealVolting_active = 1

txlevellist = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
nodelist = ['node0', 'node1', 'node2', 'node3', 'node4', 'node5', 'node6', 'node7', 'node8','node10','node11','node12','node13','node16','node17','node18']

def transmit(cli, source, dest, power, data):
	cli.write(source, "t %d %d %s" % (dest, power, data))

def volting(cli, source, switch):
	cli.write(source, "v %d" % (switch))

if __name__ == "__main__":
	seqnr = 0
	try:
		f = open(seqnrfile)
		seqnr_str = f.readline()
		seqnr = int(seqnr_str)
		print ("seqnr = " + str(seqnr))
		f.close

	except:
		print "file closed."
		seqnr = 0

		
	tbc = testbedclient.testbedclient()
#	for n in nodes:
#		print n
	while True:
#		nodes = tbc.getnodes()
		
		for node in nodelist:
			if idealVolting_active == 1:
				volting(tbc, node, 0)		
			else:
				volting(tbc, node, 1)
		time.sleep(1)
		idealVolting_active ^=1

		for node in nodelist:
			for power in txlevellist:
				print "forcing " + node + " to transmit with power " + str(power) + "..."
				transmit(tbc, node, broadcastdest, power, str(seqnr))
				seqnr += 1
				f = open(seqnrfile, "w")
				f.write(str(seqnr)+"\n")
				f.close
				time.sleep(1)
				
