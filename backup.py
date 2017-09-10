import threading
import time
import serial
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json

c = threading.Condition()
flag = 0      #shared between Thread_A and Thread_B
val = 20
coordinates = [0] # An array that stores the coordinates of the X,Y of all the Sensors.

# Server that talks to the React Theremin
class ServerToTalkToReact(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_GET(self):
        print "In GET Method"
        global coordinates
        self._set_headers()
        self.wfile.write(json.dumps(coordinates[-1])) #Sends the first co-ordinates from co-ordinate list
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

# Thread that talks to the Arduino to get the co-ordinates
class TalktoArduino(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def getDistance(self):
        ## Boolean variable that will represent
        ## whether or not the arduino is connected
        connected = False

        ## open the serial port that your ardiono
        ## is connected to.
        ser = serial.Serial("/dev/tty.usbmodem1411", 9600)

        ## loop until you get the values from the 4 sensors
        count = 0
        local_coordinates = {}
        while (1 == 1):
            if (ser.inWaiting() > 0):
                myData = ser.readline()
                print
                myData
                values = myData.split(':')
                if values[0] == 'Sensor1':  # it's at the distance 5 cms from the (0,0) graph
                    local_coordinates[values[0]] = (
                    '7.5', str(values[1]).rstrip())  # X co-ordinate is the average of range between 0 and 5
                elif values[0] == 'Sensor2':  # it's at the distance 15 cms from the (0,0) point
                    local_coordinates[values[0]] = (
                    '17.5', str(values[1]).rstrip())  # X co-ordinate is the average of range between 15 and 20
                elif values[0] == 'Sensor3':  # it's at the distance 15 cms from the (0,0) point
                    local_coordinates[values[0]] = (
                    '27.5', str(values[1]).rstrip())  # X co-ordinate is the average of range between 25 and 30
                elif values[0] == 'Sensor4':  # it's at the distance 15 cms from the (0,0) point
                    local_coordinates[values[0]] = (
                    '37.5', str(values[1]).rstrip())  # X co-ordinate is the average of range between 35 and 40
                elif values[0] == 'Sensor5':  # it's at the distance 15 cms from the (0,0) point
                    local_coordinates[values[0]] = (
                    '47.5', str(values[1]).rstrip())  # X co-ordinate is the average of range between 45 and 50
                else:
                    local_coordinates[values[0]] = (
                    '57.5', str(values[1]).rstrip())  # X co-ordinate is the average of range between 55 and 60
                count += 1
                if count > 4:
                    break
        ## close the port and end the program
        ser.close()
        return local_coordinates

    def run(self):
        print "the run in thread A"
        global flag
        global val     #made global here
        global coordinates
        while True:
            print
            "the while loop in thread A"
            c.acquire()
            if flag == 0:
                print "A: val=" , str(val)
                print "A: coordinates=" , coordinates[-1]
                time.sleep(0.1)
                flag = 1
                val = 30
                coordinates.append(self.getDistance())
                c.notify_all()
            else:
                c.wait()
            c.release()

# Thread that talks to React by spining up a web server
class TalktoReact(threading.Thread, BaseHTTPRequestHandler):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print "The run in thread B"
        server = HTTPServer(('', 8080), ServerToTalkToReact)
        thread = threading.Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()
        global flag
        global val    #made global here
        while True:
            print "The while loop in thread B"
            c.acquire()
            if flag == 1:
                print "B: value=" + str(val)
                print "B: coordinates=" , coordinates
                time.sleep(0.5)
                flag = 0
                val = 20
                c.notify_all()
            else:
                c.wait()
            c.release()


try:
    a = TalktoArduino("myThread_name_A")
    b = TalktoReact("myThread_name_B")

    b.start()
    a.start()

    a.join()
    b.join()
except:
    print
    "Error: unable to start thread"

while 1:
    pass