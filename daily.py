from slacker import Slacker
import json
import datetime

from analytics import get_report

with open('cred.json') as f:
	cred = json.load(f)
	API_TOKEN = slack_bot_token = cred['slack']['api_token']


slack = Slacker(API_TOKEN)

yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
yesterday = yesterday.strftime("%Y-%m-%d")

analytics_report = get_report('top',10,[yesterday,yesterday],'')

attachments = []
for item in analytics_report:
	attachment = {
		"fallback": item['title'].decode('utf-8') + ', pageviews: ' + item['pageviews'],
		"title": item['title'].decode('utf-8'),
		"title_link": item['url'],
		"fields": [
			{
			"title": "Page views",
			"value": item['pageviews'],
			"short": "true"
			},
			{
			"title": "Avg. time on page",
			"value": item['avg_time'],
			"short": "true"
			},
			{
			"title": "Bounce rate",
			"value": item['bounce_rate'],
			"short": "true"
			}],
		# 'color': '#36A64F'
	}
	attachments.append(attachment)

slack.chat.post_message('#smarty-playground','Hey, folks! Here are the *top 10 pages* from *yesterday*:',attachments=json.dumps(attachments),as_user='smarty')