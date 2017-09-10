## import the serial library
import serial
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json

def getDistance():
    ## Boolean variable that will represent
    ## whether or not the arduino is connected
    connected = False

    ## open the serial port that your ardiono
    ## is connected to.
    ser = serial.Serial("/dev/tty.usbmodem1411", 9600)

    ## loop until you get the values from the 4 sensors
    count = 0
    coordinates = {}
    while (1==1):
        if (ser.inWaiting()>0):
            myData = ser.readline()
            print myData
            values = myData.split(':')
            if values[0] == 'Sensor1': # it's at the distance 5 cms from the (0,0) graph
                coordinates[values[0]] = ('7.5', str(values[1]).rstrip()) # X co-ordinate is the average of range between 0 and 5
            elif values[0] == 'Sensor2': # it's at the distance 15 cms from the (0,0) point
                coordinates[values[0]] = ('17.5', str(values[1]).rstrip()) # X co-ordinate is the average of range between 15 and 20
            elif values[0] == 'Sensor3': # it's at the distance 15 cms from the (0,0) point
                coordinates[values[0]] = ('27.5', str(values[1]).rstrip()) # X co-ordinate is the average of range between 25 and 30
            elif values[0] == 'Sensor4': # it's at the distance 15 cms from the (0,0) point
                coordinates[values[0]] = ('37.5', str(values[1]).rstrip()) # X co-ordinate is the average of range between 35 and 40
            elif values[0] == 'Sensor5': # it's at the distance 15 cms from the (0,0) point
                coordinates[values[0]] = ('47.5', str(values[1]).rstrip()) # X co-ordinate is the average of range between 45 and 50
            else:
                coordinates[values[0]] = ('57.5', str(values[1]).rstrip())  # X co-ordinate is the average of range between 55 and 60
            count += 1
            if count > 4:
                break
    ## close the port and end the program
    ser.close()
    return coordinates



class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        coordinates = getDistance()
        self.wfile.write(json.dumps(coordinates))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        data = {}
        data['key'] = 'value'
        json_data = json.dumps(data)
        self.wfile.write(json_data)


def run(server_class=HTTPServer, handler_class=S, port=8081):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print
    'Starting httpd...'
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()