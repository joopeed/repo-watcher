#!/usr/bin/python2
 # -*- coding: utf-8 -*-
import BaseHTTPServer
import socket
from hooks_handler import HooksHandler

port = 8080

def run(server_class=BaseHTTPServer.HTTPServer, handler_class=BaseHTTPServer.BaseHTTPRequestHandler):
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        httpd.serve_forever()

try:
    run(BaseHTTPServer.HTTPServer, HooksHandler)
except socket.error:
    print "Server is up!"
