import time, requests, json

token=input("Enter telegram bot token:")
url = "https://api.telegram.org/bot"+token

def get_message():
    resp = requests.get(url+"/getUpdates")
    respd = json.loads(resp.content.decode("utf8"))
    new_mesg = len(respd['result'])-1
    text = respd['result'][new_mesg]["message"]["text"]
    chat_id = respd['result'][new_mesg]["message"]["chat"]["id"]
    return (text, chat_id)

def send_message(text, chat_id):
    resp = requests.get(url+"/sendMessage?text={}&chat_id={}".format(text, chat_id))

text, chat_id = get_message()
send_message(text, chat_id)
    