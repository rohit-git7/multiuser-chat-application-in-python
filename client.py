#!/usr/bin/python
import socket 
import select
import sys
#creating socket
try:
   sd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except:
   print "Error in creating socket"
   sys.exit(1)
#host and port num are given through commandline arguments
host = sys.argv[1]
port = int(sys.argv[2])

try:
   sd.connect((host,port))
except:
   print "Connection Error"
   sys.exit(1)
print "Connected to host"
while True:
   #maintaining list of descriptors who can read
   socket_list = [sys.stdin,sd]
   #select call to select the descriptor that is ready to read
   read_list,write_list,error_list = select.select(socket_list,[],[])
   #to check which descriptor is ready and take appropriate action accordingly
   for sock in read_list:
	if sock is sd:
		message = sys.stdin.readline()
		sd.send(message)
	else:
		data = sd.recv(1024)
		# no data means server has disconnected
		if not data:
			sys.stdout.write("Connection closed")
			sys.stdout.flush()
		else:
			sys.stdout.write(data)
			sys.stdout.flush()
			
