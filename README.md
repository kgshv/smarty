# smarty
Smarty is a Google Analytics / Slack bot for the [Kyiv Post](http://kyivpost.com) newsroom. Code is in **active alpha stage development**, scarce documentation and just few comments in code, use at your own risk.

## Set up

### Dependencies

I use the **slackbot**, which I found [here](https://github.com/lins05/slackbot). Thumbs up to [lins05](https://github.com/lins05)! The documentation is on the GitHub repo, I just linked. I used the development version of it, since it has more features then the master one. To install it, I pulled directly from the "develop" branch of the Git repo:

`sudo pip install git+git://github.com/lins05/slackbot@develop`

Although, you might want to just do

`sudo pip install slackbot`

That's your call.

Also, you'll need the [**Google Analytics for Python and the command-line**](https://github.com/debrouwere/google-analytics). Thanks so much to all the people behind it, by the way!. I ran:

`pip install googleanalytics`

You might also need PyOpenSSL and PyCrypto modules if you are running this on Linux (I used Ubuntu, so I'm not sure what will happen for Mac users). It has to do with Google oAuth security settings. Just google for installation instructions for your platform.

### Files
You will need some additional files. These are:

1. `cred.json`
2. `titles.json`

`titles.json` is a file solemnly for [Kyiv Post](http://kyivpost.com), to filter for page titles and not to have the bot scrape, like, the title of the home page every time. You might want to delete it, but make sure to make proper changes to the `analytics.py` if you do.

There is also the `settings.py` file. It contains some variables you might want to re-write. The file structure should be self-explanatory.

### Accounts

**Google Analytics**

You will need to get a Google Analytics **service account**, at least that's how I set it up. Google seems to change it's developer's console UI so often, that I really don't see how I can refer you to the correct place there. Start at the [Console](https://console.developers.google.com) home page and go from there to:

1. Create a new project
2. Enable the Google Analytics API
3. Generate the service account key (in my case it gave me a json file with credential information).

I deleted everything from that file except for several lines, so that my `cred.json` file has the following structure:

```javascript
{
  "analytics": {
    "private_key": "-----BEGIN PRIVATE KEY-----\n.....LOTS OF STUFF HERE........com",
    "client_id": "121212121 NUMBERS HERE"
  },
  "slack": {
    "api_token": "TOKEN CODE HERE"
  }
}
```
Notice how there's also the Slack API token there? I'll get to that in a sec, but before I do, here's another really important part.

Your `.json` file, the one, the Developer Console will generate for you, will have an email address in it. Copy it (the address will be long and might look like some_gibberish@some-email-with-google-in-it-or-something.com, that's okay)  and add it to your Google Analytics account, setting permission to read and analyze, so the service account actually has access to the proper analytics account. In theory you can allow access to multiple account (if you yourself have access to multiple ones), but I didn't explore that route.

**Slack**

Here things are more straightforward. At least IMHO. You will need to create a Slack bot account, set up an API key and add it to `cred.json`. I suggest you start from the Slack bot users [official documentation page](https://api.slack.com/bot-users) (if the link becomes dead for some reason, just google for it).

## Using smarty

This part is still in DEV MODE!

* After you run the app, in Slack open a chat with smarty (or mention it with @smarty in a channel). Say 'help' to smarty to get instructions at any time.



### ​The *report*​ syntax:

Use the keyword *report* at the beginning of the sentence to ask smarty for stats.

The `report` keyword *must* be followed by a query. You can ask for `top` start or for info on a particular `url`. In case of `top` you should then provide a number and a time period. For `url`, add the actual full url on your site, again, followed by the time period.

*Time period:*

*This can be one word or date, like `today` or `yesterday` or `2015-01-20` (that is year-month-day).
*This can be a period, separated by `from` and `to`.

### ​The *top* keyword​ syntax:

*For example*

```report top 10 today```

Will give you a list of top 10 pages, *arranged by the number of page views* (unique and non unique), from today.

```report top 5 from 2016-02-20 to yesterday```

Will give you a list of top 5 pages, *arranged by the number of page views* (unique and non unique) from February 20th, 2016 until today.

More examples:

```report top 20 today```
```report top 5 from 2015-11-10 to 2016-02-30```

The schematics is always the same: the `report` keyword, followed by `top XX` and a date or a from-to construct. Number after top ​*needs to be below or equal to 20*​.

### ​The *url* keyword​ syntax:
​
Now, if you want to get something else then a list of 10 top articles, you can also say `report url` followed by the full URL of the page you need analyzed, then also followed by the date construct.

​*For example:*​
```report url http://kyivpost.com/about-us from 28-11-2014 to today```
Will tell you all stats for the About us page on Kyiv Post for the respective time period. Make sure to use your site url and edit the titles.json, of course.