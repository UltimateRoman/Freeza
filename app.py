import requests, json

token=input("Enter telegram bot token:")
url = "https://api.telegram.org/bot"+token+"/getUpdates"
resp = requests.get(url)
mesg = json.loads(resp.content.decode("utf8"))
print(mesg['result'][1]['message']['text'])