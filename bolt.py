import json, math, statistics, time
from boltiot import Bolt

frame_size=10
mfactor=2

D_ID = input("Bolt device ID:")
A_KEY = input("API key:")

mybolt = Bolt(A_KEY, D_ID)

temp_history=[]

def threshold():
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
        thresholds = threshold()
        temp_history.append(temp)
        if not thresholds:
            rcount = frame_size-len(temp_history)
            print("Not enough data to perform Z-score analysis, require ",rcount," more data points.")
            time.sleep(10)
            continue
        print(thresholds[0],thresholds[1])
    except Exception as e:
        print(e)
        break
    time.sleep(10)