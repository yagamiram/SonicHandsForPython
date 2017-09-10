from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import threading
import time
server = HTTPServer(('', 8080), SimpleHTTPRequestHandler)
print 'OK UNTIL NOW'
thread = threading.Thread(target = server.serve_forever)
print 'STUCK HERE'
thread.daemon = True
try:
    thread.start()
except KeyboardInterrupt:
    server.shutdown()
    sys.exit(0)

print 'OK'

time.sleep(120)
