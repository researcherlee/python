#!/usr/bin/env python
'''
Created on 2009. 10. 12.

'''
import unittest
import echo_server
import getopt
import socket
import time
import os, sys
from thread import start_new_thread, get_ident

class TestEchoServer(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def run_and_check_for_option(self, testData):
        for input in testData:
            if testData[input] == getopt.error:
                self.assertRaises(getopt.error, echo_server.option_parse, input.split())
            else:                
                self.assertEquals(echo_server.option_parse(input.split()), testData[input])

    def testOptionParserTcpBasic(self):
        testData = {
            "-t -p 100 -l 10 -s 1000": (socket.SOCK_STREAM, 100, 10, 1000),
            "-t --port 101 --listeners 10 --size 1001": (socket.SOCK_STREAM, 101, 10, 1001),
            "-t -p 102": (socket.SOCK_STREAM, 102, echo_server.DEFAULT_LISTENER, echo_server.DEFAULT_PACKSIZE),
            "-t -l 103": (socket.SOCK_STREAM, echo_server.DEFAULT_PORT, 103, echo_server.DEFAULT_PACKSIZE),
            "-t -s 104": (socket.SOCK_STREAM, echo_server.DEFAULT_PORT, echo_server.DEFAULT_LISTENER,104),                                                
        }
        self.run_and_check_for_option(testData); 
        
    def testOptionParserUdpBasic(self):
        testData = {
            "-u -p 100 -l 10 -s 1000": (socket.SOCK_DGRAM, 100, 10, 1000),
            "-u --port 101 --listeners 10 --size 1001": (socket.SOCK_DGRAM, 101, 10, 1001),
            "-u -p 102": (socket.SOCK_DGRAM, 102, echo_server.DEFAULT_LISTENER,echo_server.DEFAULT_PACKSIZE),
            "-u -l 103": (socket.SOCK_DGRAM, echo_server.DEFAULT_PORT, 103, echo_server.DEFAULT_PACKSIZE),
            "-u -s 104": (socket.SOCK_DGRAM, echo_server.DEFAULT_PORT, echo_server.DEFAULT_LISTENER,104),                                                
        }
        self.run_and_check_for_option(testData);
    
    def testOptionParserBoundaryException(self):
        '''TO DO'''
        pass
        
    def testOptionParserException(self):
        testData = {
            "-t --tcp": getopt.error,
            "-u --udp": getopt.error,
            "-u --t": getopt.error,
            "-t --udp": getopt.error,
            "-tcp --udp": getopt.error,
            "-u --tcp":  getopt.error,
            "-p 10 --port 100":  getopt.error,
            "-l 10 --listeners 10":  getopt.error,
            "-s 10 --size 100":  getopt.error,
            "-zzk": getopt.error,
            "-h": getopt.error,
            "-t -s": getopt.error,                        
         }
        self.run_and_check_for_option(testData);
    
    def clients_running(self, id, type, port, pSize, threads):
        sock = socket.socket(socket.AF_INET, type)
        if type == socket.SOCK_STREAM:
            sock.connect(("127.0.0.1" ,port))
        
        for i in range(1, pSize+1):
            actual = None
            expected = str(id) * i
            if type == socket.SOCK_STREAM:
                sock.send(expected)
                actual = sock.recv(pSize)
            else:
                sock.sendto(expected, ("127.0.0.1", port))
                actual, temp = sock.recvfrom(pSize)
            self.assertEqual(actual, expected)
        sock.close()
        del threads[get_ident()]
    
    def testServerTcpBasic(self):
        threads = {}        
        server_id = start_new_thread(echo_server.run_echo_server,(socket.SOCK_STREAM, 8878, 10,1024) )
        time.sleep(1)
        for n in range(3):
            id = start_new_thread(self.clients_running, (n, socket.SOCK_STREAM,8878, 1024, threads))
            threads[id] = None
        while threads: time.sleep(.1)
    
    def testServerUdpBasic(self):
        threads = {}        
        server_id = start_new_thread(echo_server.run_echo_server, 
                                     (socket.SOCK_DGRAM, 8878, 10, 1024) )
        time.sleep(1)
        for n in range(3):
            id = start_new_thread(self.clients_running, (n,socket.SOCK_DGRAM,8878, 1024, threads))
            threads[id] = None
        while threads: time.sleep(.1)        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
