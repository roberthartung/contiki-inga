#!/usr/bin/python
import time
import testbedclient

seqnrfile = '/tmp/tmp/pn-seqnr'
broadcastdest = 65535

#TODO Update the lists
#usinga all combinatopns would take too much time
txlevellist = [0, 1, 2, 3]
channellist = [11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
nodelist = ['node0', 'node1', 'node2', 'node3', 'node4', 'node5', 'node6', 'node7', 'node8','node11','node12','node13','node14','node15','node16','node17','node18','node19']

def send_rx_command(cli, node, channel):
	cli.write(node, "rx d %d\n" % (channel))

def send_tx_command(cli, node, channel):
	cli.write(source, "tx %d sweep\n" % (channel))

def send_status_command(cli, node):
	cli.write(node, "stat\n")

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
		for channel in channellist:
			for node in nodelist:
				print "sending rx command to" + node + " with channel" + str(channel)
				send_rx_command(tbc,node,channel);

			for node in nodelist:
				print "sending tx command to" + node + " with channel" + str(channel)
				send_tx_command(tbc,node,channel);
				time.sleep(10)

			for node in nodelist:
				print "sending stat command to" + node
				send_status_command(tbc,node);
