import threading
import time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
c = threading.Condition()
flag = 0      #shared between Thread_A and Thread_B
val = 20

from SimpleHTTPServer import SimpleHTTPRequestHandler
import threading
import time

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_GET(self):
        print "In GET "
        self._set_headers()
        #coordinates = getDistance()
        #self.wfile.write(json.dumps(coordinates))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        print "In Post"
        # Doesn't do anything with posted data
        self._set_headers()
        data = {}
        data['key'] = 'value'
        json_data = json.dumps(data)
        self.wfile.write(json_data)

class Thread_A(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
    def run(self):
        server = HTTPServer(('', 8080), S)
        thread = threading.Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()
        global flag
        global val     #made global here
        while True:
            c.acquire()
            if flag == 0:
                print "A: val=" + str(val)
                time.sleep(0.1)
                flag = 1
                val = 30
                c.notify_all()
            else:
                c.wait()
            c.release()


class Thread_B(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global flag
        global val    #made global here
        while True:
            c.acquire()
            if flag == 1:
                print "B: val=" + str(val)
                time.sleep(0.5)
                flag = 0
                val = 20
                c.notify_all()
            else:
                c.wait()
            c.release()


a = Thread_A("myThread_name_A")
b = Thread_B("myThread_name_B")

b.start()
a.start()

a.join()
b.join()