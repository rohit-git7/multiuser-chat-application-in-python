#!/usr/bin/python
import socket 
import sys
import select
from gi.repository import Gtk

class TableWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Chit Chat")
	width, height = 300, 400
	self.set_size_request(width, height)
	self.set_position(Gtk.WindowPosition.CENTER)

	self.timeout_id = None

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        label1 = Gtk.Label("IP Address")
        label2 = Gtk.Label("Port")
	self.entry1 = Gtk.Entry()
        self.entry1.set_text("IP Address")
	self.entry2 = Gtk.Entry()
        self.entry2.set_text("Port Address")
        button1 = Gtk.Button("Connect")
        
        hbox = Gtk.Box(spacing=6)
        vbox.pack_start(hbox, False, True, 0)
        hbox.pack_start(label1, False, True, 0)
        hbox.pack_start(label2, True, True, 0)
	

        hbox1 = Gtk.Box(spacing=6)
        vbox.pack_start(hbox1, False, True, 0)
        
        hbox1.pack_start(self.entry1, False, True, 0)

        hbox1.pack_start(self.entry2, False, True, 0)
        
	hbox2 = Gtk.Box(spacing=6)
        vbox.pack_start(hbox2, False, True, 0)
	button1.connect("clicked", self.connect_server)
        hbox2.pack_start(button1, False, True, 0)

	scrolledwindow = Gtk.ScrolledWindow()
	scrolledwindow.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)
        scrolledwindow.set_hexpand(False)
        scrolledwindow.set_vexpand(True)
	hbox3 = Gtk.Box(spacing=6)
        vbox.pack_start(hbox3, True, True, 0)
        hbox3.pack_start(scrolledwindow, True, True, 0)

        self.textview = Gtk.TextView()
	self.textbuffer = self.textview.get_buffer()
        scrolledwindow.add(self.textview)

	self.entry3 = Gtk.Entry()
        hbox4 = Gtk.Box(spacing=6)
        vbox.pack_start(hbox4, False, True, 0)
        hbox4.pack_start(self.entry3, False, True, 0)


        button2 = Gtk.Button("Send Message")
	hbox5 = Gtk.Box(spacing=6)
        vbox.pack_start(hbox5, False, True, 0)
	button2.connect("clicked", self.send_data)
        hbox5.pack_start(button2, False, True, 0)

	
    def send_data(self, button):
	global sockfd
	if sockfd == -1:
		end_iter = self.textbuffer.get_end_iter()
  		self.textbuffer.insert(end_iter, "Connection not established.\n")	
		mark = self.textbuffer.create_mark(None, end_iter, True)	
		self.textview.scroll_to_iter(end_iter, 0.0, use_align=True,xalign=0.0, yalign=0.0)
		return
	try:
		sockfd.sendall(self.entry3.get_text())
		end_iter = self.textbuffer.get_end_iter()
  		self.textbuffer.insert(end_iter, self.entry3.get_text()+"\n")	
		mark = self.textbuffer.create_mark(None, end_iter, True)	
		self.textview.scroll_to_iter(end_iter, 0.0, use_align=True,xalign=0.0, yalign=0.0)
	except:
		end_iter = self.textbuffer.get_end_iter()
  		self.textbuffer.insert(end_iter, "Connection not established.\n")	
		mark = self.textbuffer.create_mark(None, end_iter, True)	
		self.textview.scroll_to_iter(end_iter, 0.0, use_align=True,xalign=0.0, yalign=0.0)
		
    def connect_server(self, button):
	self.entry1.set_editable(False)
	self.entry2.set_editable(False)
        if self.entry1.get_text() == "" or self.entry2.get_text() == "":
		end_iter = self.textbuffer.get_end_iter()
  		self.textbuffer.insert(end_iter, "Specify IP Address and Port correctly.\n")	
		mark = self.textbuffer.create_mark(None, end_iter, True)	
		self.textview.scroll_to_iter(end_iter, 0.0, use_align=True,xalign=0.0, yalign=0.0)
	#creating socket
	try:
		global sockfd
   		sockfd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	except:
		end_iter = self.textbuffer.get_end_iter()
  		self.textbuffer.insert(end_iter, "Error in creating socket.\n")	
		mark = self.textbuffer.create_mark(None, end_iter, True)	
		self.textview.scroll_to_iter(end_iter, 0.0, use_align=True,xalign=0.0, yalign=0.0)
		self.entry1.set_editable(True)
		self.entry2.set_editable(True)
   		return
	#host and port num are given through commandline arguments
	host = self.entry1.get_text()
	port = int(self.entry2.get_text())
	try:
  		sockfd.connect((host,port))
	except:
		end_iter = self.textbuffer.get_end_iter()
  		self.textbuffer.insert(end_iter, "Connection Error.\n")	
		mark = self.textbuffer.create_mark(None, end_iter, True)	
		self.textview.scroll_to_iter(end_iter, 0.0, use_align=True,xalign=0.0, yalign=0.0)
		self.entry1.set_editable(True)
		self.entry2.set_editable(True)
   		return
	end_iter = self.textbuffer.get_end_iter()
  	self.textbuffer.insert(end_iter, "Connected.\n\n")	
	mark = self.textbuffer.create_mark(None, end_iter, True)	
	self.textview.scroll_to_iter(end_iter, 0.0, use_align=True,xalign=0.0, yalign=0.0)

	while Gtk.events_pending():
		Gtk.main_iteration()
	val  = 0
	while True:
		while Gtk.events_pending():
			Gtk.main_iteration()
		
   		sock_list = [sockfd]
   		rd,wr,err = select.select(sock_list,[],[],0.1)
   		for sock in rd:
			if sock is sockfd:
				data = sockfd.recv(1024)
				if data:	
					end_iter = self.textbuffer.get_end_iter()
 					self.textbuffer.insert(end_iter, data+"\n")	
					mark = self.textbuffer.create_mark(None, end_iter, True)	
					self.textview.scroll_to_iter(end_iter, 0.0, use_align=True,xalign=0.0, yalign=0.0)
				else:
					end_iter = self.textbuffer.get_end_iter()
 					self.textbuffer.insert(end_iter, "Ooops! Server Down.\n")	
					mark = self.textbuffer.create_mark(None, end_iter, True)	
					self.textview.scroll_to_iter(end_iter, 0.0, use_align=True,xalign=0.0, yalign=0.0)
					
					val = -1
		if val == -1:
			break
sockfd = -1
win = TableWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
