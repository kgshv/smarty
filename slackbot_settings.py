import json
with open('cred.json') as f:
	cred = json.load(f)
	API_TOKEN = slack_bot_token = cred['slack']['api_token']

default_reply = "Sorry but I didn't understand you"

PLUGINS = [
    'slackbot.plugins'
]