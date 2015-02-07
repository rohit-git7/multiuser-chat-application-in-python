#!/usr/bin/python
 
import sys
import socket
import select

host = '' 
port = int("9009")
sock_list = []
    
# send chat messages to all connected clients
def message (server_socket, sock, message):
    for socket in sock_list:
        # send all except server and client who sent the message
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # socket connection closed
                socket.close()
                # broken socket,remove it
                if socket in sock_list:
                    sock_list.remove(socket)
 

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host,port))
server_socket.listen(10)
 
# add server socket object to the list of readable connections
sock_list.append(server_socket)
print "Server running"
 
while True:

    # get the list sockets which are ready to be read through select
    # 4th arg, time_out  = 0 : poll and never block
    ready_to_read,ready_to_write,in_error = select.select(sock_list,[],[],0)
      
    for sock in ready_to_read:
		#new connection request
        if sock == server_socket: 
            sockfd, addr = server_socket.accept()
            sock_list.append(sockfd)
            print "Client (%s, %s) connected" % addr
                 
            message(server_socket, sockfd, "[%s:%s] is here\n" % addr)
             
        # message from a client, not a new connection
        else:
            # process data received from client, 
            try:
                # receiving data
                data = sock.recv(4096)
                if data:
                    # send data
                    message(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)  
                else:
                    #remove the socket that's broken    
                    if sock in sock_list:
                        sock_list.remove(sock)

                    #no data means probably the connection has been broken
                    message(server_socket, sock, "Client (%s, %s) is offline\n" % addr) 
 
            except:
                message(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
                continue

server_socket.close()
