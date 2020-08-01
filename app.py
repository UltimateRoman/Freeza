import time, requests, json

token=input("Enter telegram bot token:")
url = "https://api.telegram.org/bot"+token

def get_message(offset):
    if offset:
        resp = requests.get(url+"/getUpdates?offset={}".format(offset))
    else:
        resp = requests.get(url+"/getUpdates")
    respd = json.loads(resp.content.decode("utf8"))
    return respd

def get_last_upid(respd):
    upids=[]
    for msg in respd['result']:
        upids.append(int(msg['update_id']))
    return max(upids)

def make_msg(respd):
    for msg in respd['result']:
        try:
            text = msg['message']['text']
            chat_id = msg['message']['chat']['id']
            send_message(text, chat_id)
        except Exception as e:
            print(e)

def send_message(text, chat_id):
    resp = requests.get(url+"/sendMessage?text={}&chat_id={}".format(text, chat_id))
    rem = json.loads(resp.content.decode("utf8"))
    print("Replied to:", rem['result']['chat']['first_name'])


def main():
    last_upid = None
    while True:
        try:
            respd = get_message(last_upid)
            if len(respd['result'])>0:
                last_upid = get_last_upid(respd)+1
                make_msg(respd)
            time.sleep(1)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()