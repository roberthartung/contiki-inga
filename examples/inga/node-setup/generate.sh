#!/bin/bash

for i in `seq 0 19`; do
	make TARGET=inga clean
	make TARGET=inga REV=1.6.1 PAN_ADDR=$i inga-setup.hex
	mv inga-setup.hex inga-setup-$i.hex
done
