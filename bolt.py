import json, math, statistics, time
from boltiot import Bolt

frame_size=10
mfactor=3
open=False

D_ID = input("Bolt device ID:")
A_KEY = input("API key:")

mybolt = Bolt(A_KEY, D_ID)

def device_status():
    statmesg = mybolt.isOnline()
    status = json.loads(statmesg)
    if status['value'] == 'online':
        return True
    else:
        return False

def get_temp():
    resp = mybolt.analogRead('A0')
    tempd = json.loads(resp)
    if not tempd['success']:
        return None
    else:
        temp = int(tempd['value'])/10.24
        return temp

temp_history=[]

def set_threshold():
    if len(temp_history) < frame_size:
        return None
    if len(temp_history) > frame_size:
        del temp_history[0:len(temp_history)-frame_size]
    mean = statistics.mean(temp_history)
    variance = 0
    for t in temp_history:
        variance += math.pow((t-mean),2)
    zn = mfactor*math.sqrt(variance/frame_size)
    upr_limit = temp_history[frame_size-1]+zn
    lwr_limit = temp_history[frame_size-1]-zn
    return [upr_limit, lwr_limit]

def is_open(temp, thresholds):
    if temp > thresholds[0]:
        return True
    else:
        return False

while True:
    try:
        online = device_status()
        if not online:
            print("Device is offline or rate limited!")
            break
        temp = get_temp()
        if not temp:
            print("Request unsucessfull!")
            break
        print(temp)
        thresholds = set_threshold()
        if not thresholds:
            temp_history.append(temp)
            rcount = frame_size-len(temp_history)
            print("Not enough data to perform Z-score analysis, require ",rcount," more data points.")
            time.sleep(10)
            continue
        open = is_open(temp, thresholds)
        if not open:
            temp_history.append(temp)
            mybolt.digitalWrite(1, 'LOW')
        else:
            print("Refrigerator open")
            mybolt.digitalWrite(1, 'HIGH')
        print(thresholds[0],thresholds[1])
    except Exception as e:
        print(e)
        break
    time.sleep(10)