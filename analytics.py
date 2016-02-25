import json
import googleanalytics as ga
import urllib2
import re
from math import floor

from settings import GA_PROFILE

with open('cred.json') as f:
	cred = json.load(f)

accounts = ga.authenticate(**cred['analytics'])
profile = accounts[0].webproperties[GA_PROFILE].profile

def get_report(word,top_number,from_to_dates, path):

	query = profile.core.query.total(from_to_dates[0],from_to_dates[1])

	if top_number > 20:
		top_number = 20
	elif top_number <= 0:
		top_number = 10

	if word == 'top':
		result = query.dimensions('ga:pagePath').metrics('pageviews', 'unique pageviews', 'ga:avgTimeOnPage', 'ga:bounceRate', 'entrances', 'exits').sort('pageviews', descending=True).limit(top_number)
	else:
		result = query.dimensions('ga:pagePath').metrics('pageviews', 'unique pageviews', 'ga:avgTimeOnPage', 'ga:bounceRate', 'entrances', 'exits').sort('pageviews', descending=True).limit(top_number).filter(pagepath=path)

	with open('titles.json') as t:
		titles = json.load(t)

	response = []

	# for every page in top *top_number* visited pages:
	for row in result.report.rows:
		url = str(row.page_path)
		if url in titles:
			title = titles[url]
			full_url = 'http://kyivpost.com/'
		else:
			full_url = 'http://kyivpost.com' + url
			page = urllib2.urlopen(full_url).read()
			title = str(page).split('<title>')[1].split('</title>')[0]
			title = title.replace('\n','')
			# get rid of extra spaces, if those exist
			p = re.compile('([\s]{2,})(.*)')
			try:
				title = re.search(p,title).group(2)
			except AttributeError:
				title = 'some title here'
				pass

		# calculate proper average time in minutes (given in seconds)
		minutes = int( floor( (row.avg_time_on_page / 60) % 60 ) )
		seconds = int( floor(row.avg_time_on_page % 60) )
		avg_time = '{m}:{s}'.format(m=minutes,s=seconds)

		bounce_rate_pct = str( int( round( row.bounce_rate ) ) ) + '%'

		record = {
			'title': title,
			'url' : full_url,
			'pageviews': str(row.pageviews),
			'avg_time': avg_time,
			'bounce_rate': bounce_rate_pct,
		}

		response.append(record)

	return response

def get_by_id(id):
	return ''