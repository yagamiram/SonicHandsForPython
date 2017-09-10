import os
import sys
import pprint
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from m2x.client import M2XClient


KEY = os.environ['KEY']
DEVICE_ID = os.environ['DEVICE']

client = M2XClient(key=KEY)
device = client.device(DEVICE_ID)
stream = device.stream('musicCreator')
pprint.pprint(device.data)

# And now register the current time every 10 seconds (hit ctrl-c to kill)
while True:
    print int(time.time())
    stream.add_value(int(time.time()))
    time.sleep(10)