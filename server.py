#  coding: utf-8 
import socketserver
import os.path
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

# curl -v -X -i GET http://127.0.0.1:8080/
#https://stackoverflow.com/questions/41852380/how-to-abort-a-python-script-and-return-a-404-error


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        error_404 = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n <html><head></head><body><h1>404 Not Found</h1></body></html>"
        error_405 = "HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html\r\n\r\n <html><head></head><body><h1>405 Method Not Allowed</h1></body></html>"
        request_200_html = "HTTP/1.1 200 OK \r\nContent-Type: text/html\r\n\r\n"
        request_200_css = "HTTP/1.1 200 OK \r\nContent-Type: text/css\r\n\r\n"
        request_301 = "HTTP/1.1 301 Moved Permanently \r\nLocation: "

        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        split = self.data.decode("utf-8").split()
        # print("\\index.html")
        if split[0]=="GET":
            # print(split[1][-1:])
            path = 'www'+split[1]


            if os.path.isfile(path) or os.path.isdir(path):
                # print(split[1][-1:])
                if split[1][-1:] == "/":
                    path = path + 'index.html'
                    good = request_200_html+open(path,'r').read()
                    self.request.sendall(bytearray(good,'utf-8'))
                else:
                    # print('\n HEY: ', split[1][-4:] )
                    if split[1][-4:] == 'html':
                        good = request_200_html+open(path,'r').read()
                        self.request.sendall(bytearray(good,'utf-8'))
                    elif split[1][-3:] == 'css':
                        good = request_200_css+open(path,'r').read()
                        # print(good)
                        self.request.sendall(bytearray(good,'utf-8'))
                    else:
                    	#redirect if / is missing
                    	print("e")
                    	if os.path.isfile(path + '/index.html'):
                    		# ***change to redirect
                    		# this should work because it checks if there is 
                    		#the file in the directory - it is likning
                    		#to deep - but it the abs path isnt there it wont
                    		#go into the if statement
                    		print("it should be here ")
                    		good = request_301+ path + "/ \r\n\r\n"+open(path+'/index.html','r').read()
                    		self.request.sendall(bytearray(good,'utf-8'))
                    	else:
                        	self.request.sendall(bytearray(error_404,'utf-8'))
                # else:
                #     good = request_200_html+index_base.read()
                #     self.request.sendall(bytearray(good,'utf-8'))
            elif os.path.isfile(path+'index.html'):
                # print(split[1][-1:])
                if split[1][-1:] == "/":
                    path = path + 'index.html'
                    # print(path)
                    good = request_200_html+open(path,'r').read()
                    self.request.sendall(bytearray(good,'utf-8'))
            else:
                self.request.sendall(bytearray(error_404,'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
