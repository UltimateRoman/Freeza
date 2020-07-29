import json, time
from boltiot import Bolt

D_ID = input("Bolt device ID:")
A_KEY = input("API key:")

mybolt = Bolt(A_KEY, D_ID)

while True:
    statmesg = mybolt.isOnline()
    status = json.loads(statmesg)
    if status['success']:
        temp = mybolt.analogRead('A0')
    time.sleep(10)