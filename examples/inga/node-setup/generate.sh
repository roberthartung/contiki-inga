#!/bin/bash

for i in `seq 0 19`; do
	make TARGET=inga clean
	make TARGET=inga REV=1.6.1 PAN_ADDR=$i SETTINGS_SET_LOAD=1 SETTINGS_DELETE_LOAD=0 inga-setup.hex 
	mv inga-setup.hex inga-setup-$i.hex
done

scp -P 2522 inga-setup-*.hex potato@thunder:~/pdr-test/
