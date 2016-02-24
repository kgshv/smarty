from slackbot.bot import Bot, respond_to, listen_to
import re
import json
import time
import random
from settings import COMPANY_NAME, EXAMPLE_URL, EXAMPLE_URL_TITLE, DOMAIN_NAMES
from analytics import get_report

import sys

def main():
	bot = Bot()
	bot.run()




@respond_to("^hi|^hello|^hi there|^what's up", re.IGNORECASE)
def hi(message):
	responses = ['Hello','Hello there','Hi there','Sup','Hey']
	message.reply(random.choice(responses))


@respond_to('^help', re.IGNORECASE)
def help(message):

		reply = 'The *report* syntax: \n\
>You can say things like `report top 10 yesterday` or `report top 20 today` or \
`report top 5 from 10-11-2015 to 30-02-2016`. That is date-month-year.\n\
The schematics is always the same: the `report` keyword, followed by `top 10` \
and a date or a from-to construct. Number after top *needs to be below or equal to 20*.\n\
*Types of reports:*\n\
>Now, if you want to get something else then a list of 10 top articles, \
you can also say `report url` followed by the full URL of the page on '+COMPANY_NAME+' you need analyzed and the date construct.\n\
So, *for example:*\n\
```report url '+EXAMPLE_URL+' from 28-11-2014 to today```\n\
Will tell you all stats for the '+EXAMPLE_URL_TITLE+' page on '+COMPANY_NAME+' for the respective time period.'

		message.reply(reply)

def extract_dates(request):
	def getDates(r):
		keys = r.split(" ")
		date_to = keys[-1]
		date_from = keys[-3]
		return [date_from,date_to]		

	if ' from ' in request:
		from_to_dates = getDates(request)
	else:
		words = request.split(" ")
		date = words[-1]
		from_to_dates = [date, date]
		
	return from_to_dates

def AnalyticsParams(word, request):
	'''If words "top" or "url" in request'''

	from_to_dates = extract_dates(request)

	p = re.compile('(%s)(\s)(\S*)' % word)
	result = re.search(p,request)

	if word == 'top':
		top_number = int(result.group(3))
		page_path = ''
	else: # that is if word is "url"
		top_number = 1
		page_path = result.group(3)
		# get rid of the domain name
		for name in DOMAIN_NAMES:
			page_path = page_path.replace(name,'')
		page_path = page_path.replace('<','').replace('>','')

	analytics_request_params = {
		'word': word,
		'top_number': top_number,
		'from_to_dates': from_to_dates,
		'path': page_path
	}

	return analytics_request_params

@respond_to('report(.*)', re.IGNORECASE)
def report_with_details(message, request):

	if request == '':
		message.reply('Please specify a date or a time frame. Type "help" for details.')
	else:
		message.reply('Just a sec, working...')
		try:
			if ' top ' in request:
				params = AnalyticsParams('top',request)
			else: # that is if url in request
				params = AnalyticsParams('url',request)

			analytics_report = get_report(**params)

			attachments = []
			raiting = 0
			for item in analytics_report:
				raiting += 1
				attachment = {
					'fallback': str(raiting),	
					'text': 'Page: ' + item['title'].decode('utf-8'),
					"fields": [
						{
						"title": "Rating: ",
						"value": str(raiting),
						"short": "true"
						},
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

			if ' top ' in request:
				message.reply('Okay, here are the *top '+str(params['top_number'])+' stories, time span is: '+params['from_to_dates'][0]+' - '+params['from_to_dates'][1]+ '*')
			else:
				message.reply('Okay, here are the *stats for the single page you requested, time span is: '+params['from_to_dates'][0]+' - '+params['from_to_dates'][1]+ '*')
			message.send_webapi('', json.dumps(attachments))

		except:
			# e = sys.exc_info()[0]
			message.reply('Oops. Looks like something went wrong. Are you sure you formated your query correctly? Type "help" for instructions.')
			# message.reply(e)



# @respond_to('reported', re.IGNORECASE)
# def report(message):

# 	message.reply('Just a sec, working')

# 	analytics_report = get_report_yesterday()

# 	attachments = []
# 	raiting = 0
# 	for item in analytics_report:
# 		raiting += 1
# 		attachment = {
# 			'fallback': str(raiting),	
# 			'text': 'Page: ' + item['title'].decode('utf-8'),
# 			"fields": [
# 				{
# 				"title": "Rating: ",
# 				"value": str(raiting),
# 				"short": "true"
# 				},
# 				{
# 				"title": "Page views",
# 				"value": item['pageviews'],
# 				"short": "true"
# 				},
# 				{
# 				"title": "Avg. time on page",
# 				"value": item['avg_time'],
# 				"short": "true"
# 				},
# 				{
# 				"title": "Bounce rate",
# 				"value": item['bounce_rate'],
# 				"short": "true"
# 				}],
# 			# 'color': '#36A64F'
# 		}
# 		attachments.append(attachment)

# 	message.reply('Okay, here are the *top 10 stories from yesterday*')
# 	message.send_webapi('', json.dumps(attachments))


if __name__ == "__main__":
	main()