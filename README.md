# smarty
Smarty is a Google Analytics / Slack bot for the [Kyiv Post](http://kyivpost.com) newsroom. Code is in **active alpha stage development**, scarce documentation and just few comments in code, use at your own risk.

## Set up

### Dependencies

I use the **slackbot**, which I found [here](https://github.com/lins05/slackbot). Thumbs up to [lins05](https://github.com/lins05)! The documentation is on the GitHub repo, I just linked. I just ran this:

`sudo pip install slackbot`

Also, you'll need the **Google Analytics for Python and the command-line**, which is [here](https://github.com/debrouwere/google-analytics) (Thanks so much to all the people behind it!). I ran:

`pip install googleanalytics`

### Files
You will need some additional files. These are:

1. `cred.json`
2. `titles.json`

`titles.json` is a file solemnly for [Kyiv Post](http://kyivpost.com), to filter for page titles and not to have the bot scrape, like, the title of the home page every time. You might want to delete it, but make sure to make proper changes to the `analytics.py` if you do.

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
Notice how there's also the Slack API token there? I'll get to that in a sec, but before I do, here's another really important part. Your .json file, the one, the Developer Console will generate for you, will have an email address in it. Copy it (the address will be long and might look like some_gibberish@some-email-with-google-in-it-or-something.com, that's okay)  and add it to your Google Analytics account, setting permission to read and analyze, so the service account actually has access to the proper analytics account. In theory you can allow access to multiple account (if you yourself have access to multiple ones), but I didn't explore that route.

**Slack**

Here things are more straightforward. At least IMHO. You will need to create a Slack bot account, set up an API key and add it to `cred.json`. I suggest you start from the Slack bot users [official documentation page](https://api.slack.com/bot-users) (if the link becomes dead for some reason, just google for it).

## Using smarty.

I will write this part as soon as I finish the bot itself.