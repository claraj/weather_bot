## Weatherbot

Check the forecast high temp for 60 major US cities. Which one has the lowest high temperature for the day, and is it Minneapolis-St. Paul?

A Twitter Bot running on Google App Engine, and tweeting daily here: https://twitter.com/mpls_most_cold

### Installation

Create a Google account. Create a project. Download and install Python Google App Engine SDK, as directed here: https://cloud.google.com/appengine/docs/python/quickstart

GAE uses Python 2.7. Macs have this installed by default, PCs may need to install it.

You'll need to enable billing at Google App Engine (GAE), with a credit card, to be able to use Tweepy to tweet over HTTPS. This application is well within the free tier. Without needing Tweepy, this app would run without billing enabled.

Create a developer account at Twitter. Create an application, and create the keys and secrets.

Create a developer account at Weather Underground. Create an application and request a key.

Provide a file called keys.py in the root directory with this format. Replace the XXXXXXX with your keys and secrets.

```

keys = { 'WEATHER_UNDERGROUND' : 'XXXXXXX',
'TWITTER_CONSUMER_KEY' : 'XXXXXXXXXXXXX',
'TWITTER_CONSUMER_SECRET' : 'XXXXXXXXXXXXX',
'TWITTER_ACCESS_TOKEN' :'XXXX-XXXXXXXX',
'TWITTER_ACCESS_TOKEN_SECRET' : 'XXXXXXXXXXXXX'
 }
```

Install the dependencies with

```
pip install -r requirements.txt -t lib/
```

And then deploy to your GAE project, deploy the app, queue and cron job yaml configuration.

```
gcloud app deploy
gcloud app deploy cron.yaml queue.yaml
```

It should tweet at about 9.15am every morning, US Central Time.

### Notes

Note: for various reasons (no cron jobs, pytz not available...), this doesn't work in the development server, it needs to be deployed to your GAE project.

WU limits use of the free API to 10 calls per minute, so the calls are throttled. GAE won't let regular requests run for more than 1 minute, so the API call task is in a task queue, which are permitted to run for up to 10 minutes. In future, may replace with a different weather API (National Weather Service, Open Weather Map?)

Logging  (not calling the print function) is a good idea. The GAE console has got loads of useful data for debugging your app.
