import tweepy
from keys import keys
import webapp2
import logging
from google.appengine.api import taskqueue

import get_weather


class QueueRequest(webapp2.RequestHandler):

    def get(self):
        taskqueue.add(
            url='/weather',
            target='main'
        )

        logging.info('Weather forecast requests task enqueued')
        self.response.write('Weather forecast task enqueued.')


class WeatherBotHandler(webapp2.RequestHandler):

    def post(self):

        high_temps = get_weather.get_forecast_highs()

        # What's the lowest high temperature?
        lowest_high_city, lowest_high_temp = get_weather.lowest_high_temp(high_temps)

        # Is it Minneapolis or St. Paul? (St. Paul is not in the city list, but keep this condition in case we put it back)

        if 'Minneapolis' in lowest_high_city or 'St. Paul' in lowest_high_city:
            # Our high temp is the coldest.
            tweet_text = '*** Today, Minneapolis-St. Paul has the coldest high temperature of any major US city, %.1fC.' % lowest_high_temp
        else:
            tweet_text =  'Minneapolis-St. Paul is not the coldest. Today, it\'s %s with a forecast high of %.1fC' % ( lowest_high_city, lowest_high_temp)


        logging.info('About to tweet: ' + tweet_text)

        try:

            auth = tweepy.OAuthHandler(keys['TWITTER_CONSUMER_KEY'], keys['TWITTER_CONSUMER_SECRET'] )
            auth.set_access_token(keys['TWITTER_ACCESS_TOKEN'], keys['TWITTER_ACCESS_TOKEN_SECRET'] )
            api = tweepy.API(auth)

            api.update_status(tweet_text)

            logging.info('tweepy has tweeted successfully')

        except Exception as e:
            # log error
            logging.error(str(e))
            raise e


        self.response.set_status(201)   # Success, no content needs to be sent.
        #self.response.write('Just attempted to tweet %s ' % tweet_text)



app = webapp2.WSGIApplication([
    ('/weather', WeatherBotHandler),
    ('/go', QueueRequest)
])
