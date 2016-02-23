import json
import googleanalytics as ga
import urllib2
import re
from math import floor

from settings import PROFILE

with open('cred.json') as f:
	cred = json.load(f)

accounts = ga.authenticate(**cred['analytics'])
profile = accounts[0].webproperties[PROFILE].profile


def get_report_yesterday():

	query = profile.core.query.daily(days=-1)

	result = query.dimensions('ga:pagePath').metrics('pageviews', 'unique pageviews', 'ga:avgTimeOnPage', 'bounces', 'entrances', 'exits').sort('pageviews', descending=True)

	with open('titles.json') as t:
		titles = json.load(t)

	response = []

	# for every page in top 10 visited pages:
	for row in result.report.rows[0:9]:
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
				pass

		# calculate proper average time in minutes (given in seconds)
		minutes = int( floor( (row.avg_time_on_page / 60) % 60 ) )
		seconds = int( floor(row.avg_time_on_page % 60) )
		avg_time = '{m}:{s}'.format(m=minutes,s=seconds)

		bounce_rate_pct = str( int( round( ((row.bounces*100)/row.entrances) ) ) ) + '%'

		record = {
			'title': title,
			# 'url' : full_url,
			'pageviews': str(row.pageviews),
			'avg_time': avg_time,
			'bounce_rate': bounce_rate_pct,
		}

		response.append(record)

	return response

def get_by_id(id):
	return ''