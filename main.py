import tweepy
import keys
import webapp2

import get_weather

class WeatherBotHandler(webapp2.RequestHandler):

    def get(self):

        highs_temps = get_weather.get_forecast_highs()
        high_temps = {'San_Bernardino': -15.0, 'Gilbert': 15.0, 'Birmingham': 22.0, 'Boise': -6.0}

        # What's the lowest high?

        lowest_high_temp = 1000
        lowest_high_city = ''
        for city in high_temps:
            if high_temps[city] < lowest_high_temp:
                lowest_high_temp = high_temps[city]
                lowest_high_city = city

        # Is it Minneapolis?

        tweet_text = ''

        snowflake = '\u2744' * 2

        if 'Minneapolis' in lowest_high_city or 'St. Paul' in lowest_high_city:
            # Our high temp is the coldest.
            tweet_text = snowflakes + 'Today, Minneapolis-St. Paul has the coldest high temperature of any major US city, %.1f.' % lowest_high_temp
        else:
            tweet_text =  snowflake + 'Minneapolis-St. Paul is not coldest. Today, it\'s %s with a forecast high of %.1f' % ( lowest_high_city, lowest_high_temp)


        try:
            auth = tweepy.OAuthHandler(keys['TWITTER_CONSUMER_KEY'], keys['TWITTER_CONSUMER_SECRET'] )
            auth.set_access_token(keys['TWITTER_ACCESS_TOKEN'], keys['TWITTER_ACCESS_TOKEN_SECRET'] )

            api = tweepy.API(auth)

            api.update_status(tweet_text)

        except:
            # log error
            print('an error tweeting!')


        #self.response.set_status(201)
        self.response.write('sdfsfd')





app = webapp2.WSGIApplication([
    ('/', WeatherBotHandler)
])
