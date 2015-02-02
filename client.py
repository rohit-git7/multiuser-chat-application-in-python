#!/usr/bin/python
import socket
import select
import sys
try:
   sd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except:
   print "Error in creating socket"
   sys.exit(1)

host = sys.argv[1]
port = int(sys.argv[2])

try:
   sd.connect((host,port))
except:
   print "Connection Error"
   sys.exit(1)
print "Connected to host"
while True:
   socket_list = [sys.stdin,sd]
   read_list,write_list,error_list = select.select(socket_list,[],[])
   
   for sock in read_list:
	if sock is sd:
		message = sys.stdin.readline()
		sd.send(message)
	else:
		data = sd.recv(1024)
		if not data:
			sys.stdout.write("Connection closed")
			sys.stdout.flush()
		else:
			sys.stdout.write(data)
			sys.stdout.flush()
			
