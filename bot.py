from slackbot.bot import Bot, respond_to, listen_to
import re
from analytics import get_report_yesterday

def main():
	bot = Bot()
	bot.run()

@respond_to('hi', re.IGNORECASE)
def hi(message):
	message.reply('Ask something else, please.')

@respond_to('report', re.IGNORECASE)
def report(message):

	message.reply('Just a sec, working...')

	analytics_report = get_report_yesterday()

	reply = '*Smarty reporting!*\n'
	reply += 'Information from yesterday: \n' + ' ' + '\n'
	for item in analytics_report:
		reply+='*Page:* `' + item['title'].decode('utf-8') + '`\n' \
		+ '    *Page views:* `' + item['pageviews'] + '`\n' \
		+ '    *Average time on this page:* `' + item['avg_time'] + '`\n' \
		+ '    *Bounce rate:* `' + item['bounce_rate'] + '`\n'
	message.reply(reply)

@listen_to('Can someone help me?')
def help(message):
	# Message is replied to the sender (prefixed with @user)
	message.reply('Yes, I can!')


if __name__ == "__main__":
	main()