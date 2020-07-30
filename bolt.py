import json, time
from boltiot import Bolt

D_ID = input("Bolt device ID:")
A_KEY = input("API key:")

mybolt = Bolt(A_KEY, D_ID)

while True:
    try:
        statmesg = mybolt.isOnline()
        status = json.loads(statmesg)
        if status['value'] == 'offline':
            print("Device is offline!")
            break
        resp = mybolt.analogRead('A0')
        tempd = json.loads(resp)
        if not tempd['success']:
            print("Request unsucessfull!")
            break
        temp = int(tempd['value'])/10.24
        print(temp)
        mybolt.digitalWrite(1, 'HIGH')
        time.sleep(5)
        mybolt.digitalWrite(1, 'LOW')
    except Exception as e:
        print(e)
        break
    time.sleep(10)