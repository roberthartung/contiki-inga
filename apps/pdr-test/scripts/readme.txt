Python Scripts to orchestrate the Evaluation on the PotatoNet:
-----------------------------------------------------------------

eval_logging

Implementation of a virtual UART connection from the WRTnode to the xcentral box.
The central box executes the server.py, while the nodes run the logging_client.py. 
The nodes are registered by using the mac address which are defined in the  testbed.yaml

eval_director

script to orchestrate the evaluation.
By using the virtual uart connection, the specific commands are send to the nodes.   
