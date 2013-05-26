#!/usr/bin/env python

"""
File name: echo_server.py

  An echo server that uses select to handle multiple clients at a time.
  Entering any line of input at the terminal will exit the server.

Requires: 
   Installed Python 2.6 over

 Inspired by:
   http://ilab.cs.byu.edu/python/select/echoserver.html

 Usage:
   Refer to the 'usage_string' in source code in below
   You can also see the usage to run "python echo_server.py" (without 
any options)

Created on 2009. 10. 9.
"""

import select
import socket
import sys
import getopt
import string

#### Global variables ####
usage_string = """
Usage: python echo_server.py (-t|-u) [-p number [-l number [-s number]]]

options:
  -t, --tcp        Uses TCP protocol in running echo server.
  -u, --udp        Uses UDP protocol in running echo server.
  -p, --port       Port number that the echo server uses.
                   Default value is "8081"
  -l, --listeners  Maximun client numbers that server can accept at the 
same time.
                   Default value is "5"
  -s, --size       The size of packet the server treats at a one chunk.
                   Default value is "2048"

examples:
  1) Run the tcp echo server at default (8081) port.  
       >> python echo_server.py -t
                
  2) Run the udp echo server at 1000 port, 
     which can accept up to 10 clients and process 1024 bytes at one 
chunk.
       >> python echo_server.py -u -p 1000 -l 10 -s 1024
        
Report bugs to <reliableeleelee@samsung.com> or <reliableelee@gmail.com>
"""
DEFAULT_PORT = 8081
DEFAULT_LISTENER = 5
DEFAULT_PACKSIZE = 2048
########################


def error():
    print usage_string
    sys.exit(0)
    
def option_parse(args):
    socketType = port = listeners = packSize = None    
    opts, args = getopt.getopt(args, "tup:l:s:", ["tcp", "udp" , 
"port=", "size=", "listeners="])
        
    for o, v in opts:
        if o in ("-t", "--tcp") and socketType == None:
            socketType = socket.SOCK_STREAM
        elif o in ("-u", "--udp") and socketType == None:
            socketType = socket.SOCK_DGRAM
        elif o in ("-p", "--port") and v != "" and port == None:
            port = int(v)
        elif o in ("-l", "--listeners") and v != "" and listeners == None:
            listeners = int(v)
        elif o in ("-s", "--size") and v!= "" and packSize == None:
            packSize = int(v)
        else:
            raise getopt.error("ERROR in %s, %s option" % (o, v))
    if socketType == None: raise getopt.error("SOCKET TYPE (-t or -u) is required")
    if port == None: port = DEFAULT_PORT
    if listeners == None: listeners = DEFAULT_LISTENER
    if packSize == None: packSize = DEFAULT_PACKSIZE
    
    return socketType, port, listeners, packSize

def run_echo_server(socketType, port, listeners, packSize):
    
    isTCP =( socketType == socket.SOCK_STREAM)       
            
    host = ''
    server = socket.socket(socket.AF_INET, socketType)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    server.bind((host,port))
    if isTCP:
        server.listen(listeners)
    
    # for getting the local address
    testsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    testsocket.settimeout(1)
    testsocket.connect(("samsung.net", 80))
    
    print "Started Echo server that echos the client's request, "
    print "with printing first byte and ending byte of the packet in the server monitor."
    print "Input 'q' to quit if you are using unix-based OS, or, on Windows, input '^C' to finish\n"
    
    print "Server configuration------------"
    print " - Server Type: %s" % (isTCP and "TCP" or "UDP")
    print " - Server Addr: %s:%d" % (testsocket.getsockname()[0], port)
    print " - Packet Size: %d" % packSize
    print " - Max Allowed Clients: %s" % (isTCP and str(listeners) or 
"N/A in UDP")
    print "--------------------------------"   
    del testsocket
    
      
    input = [server, sys.stdin]
    if sys.platform == "win32" or sys.platform == "cygwin":
        input.pop()
        
    running = True
    while running:
        inputready,outputready,exceptready = select.select(input,[],[])
        for s in inputready:
            if s == server and isTCP:
                # handle the server socket
                client, address = server.accept()
                input.append(client)
                print "Accpeted new client from %s:%d" % ( client.getpeername()[0], client.getpeername()[1])
                print "Clients list currently being serviced: ",
                print "[", " ,".join([ "%s:%d" % (c.getpeername()[0], 
c.getpeername()[1]) 
                                      for c in input if c != sys.stdin 
and c != server ] ),
                print "] "

            elif s == sys.stdin:
                # handle standard input
                junk = sys.stdin.readline()
                if junk=='q\n': running = False

            else:
                # handle all other sockets
                try:
                    data = peerAddr = None
                    if isTCP:
                        data = s.recv(packSize)
                        peerAddr = s.getpeername()
                    else:
                        data, peerAddr = s.recvfrom(packSize)
                    if not data: raise socket.error
                    startStr = data[0] in string.printable and data[0] or "?"
                    endStr = data[-1] in string.printable and data[-1] or "?" 
                    
                    print "received size from %s:%d = %d byte of \"%s(%s)...%s(%s)\"" % (
                                                        peerAddr[0], peerAddr[1], len(data),
                                                        hex(ord(data[0])), startStr, hex(ord(data[-1])), endStr)
                    
                    if isTCP:
                        s.send(data)
                    else:
                        s.sendto(data, peerAddr)
                except socket.error:
                    if isTCP:
                        print "one of the clients was disconnected" 
                        s.close()
                        input.remove(s)
                        print "Clients list currently being serviced: ",
                        print "[ ", " ,".join([ "%s:%d" % 
(c.getpeername()[0], c.getpeername()[1]) 
                                      for c in input if c != sys.stdin 
and c != server ] ),
                        print " ]"
                    else:
                        print "Warning: Communication error in UDP"
    server.close()
    print "\nFinish the program.." 

if __name__ == "__main__":
    try:
        socketType, port, listeners, packSize = option_parse(sys.argv[1:])
        run_echo_server(socketType, port, listeners, packSize)
    except getopt.error:
        error()
        sys.exit(1)
    except  ValueError:
        error()
        sys.exit(1)        
    except KeyboardInterrupt:
        print "\nFinish the program.."

