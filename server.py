#  coding: utf-8 
import socketserver

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

#https://stackoverflow.com/questions/41852380/how-to-abort-a-python-script-and-return-a-404-error


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        error_404 = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n <html><head></head><body><h1>404 Not Found</h1></body></html>"
        error_405 = "HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html\r\n\r\n <html><head></head><body><h1>405 Method Not Allowed</h1></body></html>"
        request_200_html = "HTTP/1.1 200 OK \r\nContent-Type: text/html\r\n\r\n"
        request_200_css = "HTTP/1.1 200 OK \r\nContent-Type: text/css\r\n\r\n"
        
        index_base = open('www/index.html','r')
        base_css = open('www/base.css')

        index_deeper = open('www/deep/index.html','r')
        deeper_css = open('www/deep/deep.css','r')

        index_base_hardcode = open('www/hardcode/index.html','r')
        index_css_hardcode = open('www/hardcode/deep.css','r')


        test = 'www'

        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        split = self.data.decode("utf-8").split()
        # print("\\index.html")
        if split[0]=="GET":

            # test2 = open(test+split[1],'r') 

            if split[1] == "/index.html"or split[1] == "/":
                # print("valid response",split[1])
                good = request_200_html+index_base.read()
                self.request.sendall(bytearray(good,'utf-8'))
            elif split[1] == "/base.css":
                good = request_200_css+base_css.read()
                # print(good)
                self.request.sendall(bytearray(good,'utf-8'))
            elif split[1] == "/deep/index.html" or split[1] == "/deep/":
                good = request_200_html+index_deeper.read()
                # print(good)
                self.request.sendall(bytearray(good,'utf-8'))
            elif split[1] == "/deep/deep.css": 
                good = request_200_css+deeper_css.read()
                # print(good)
                self.request.sendall(bytearray(good,'utf-8'))
            elif split[1] == "/hardcode/index.html" or split[1] == "/hardcode/": 
                 good = request_200_html+index_base_hardcode.read()
                 self.request.sendall(bytearray(good,'utf-8'))
            elif split[1] == "/hardcode/deep.css": 
                 good = request_200_css+index_css_hardcode.read()
                 self.request.sendall(bytearray(good,'utf-8'))
            else:
                # print("error\n\n")
                self.request.sendall(bytearray(error_404,'utf-8'))
        else:
            self.request.sendall(bytearray(error_405,'utf-8'))
            #print("error:", split) 
        # print(split)

        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
