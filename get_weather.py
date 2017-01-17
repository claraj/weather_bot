from keys import keys
from time import sleep
import urllib2
import logging

import json
import os

sleepdelay = 65
key = keys['WEATHER_UNDERGROUND']

city_list_file = os.path.join('data', 'city_data.txt')

url_base = 'http://api.wunderground.com/api/%s/forecast/q/%s/%s.json'

def get_weather(url, city, state):

    response = urllib2.urlopen(url)
    text = response.read()
    json_response = json.loads(text)

    return json_response


def get_high(response):
    ''' get the high temp from the json'''
    try:
        high = response["forecast"]["simpleforecast"]["forecastday"][0]['high']['celsius']
        return float(high)
    except KeyError:
        logging.warning('Key error reading the following JSON ' + str(response))
        return None


def get_forecast_highs():

    with open(city_list_file, 'r') as f:
        cities = f.readlines()

    rate_limiter = 0

    todays_forecast_highs = {}

    for entry in cities:

        rate_limiter += 1

        logging.info('Query %d fetching data for %s' % (rate_limiter, entry))

        if rate_limiter % 10 == 0:
            logging.info('sleeping for %s seconds' % sleepdelay)
            sleep(sleepdelay)

        city = entry.split('; ')[0].replace(' ', '_')
        state = entry.split('; ')[1].strip()

        url = url_base % ( key, state, city)

        resp = get_weather(url, city, state)
        high_temp = get_high(resp)

        if high_temp is not None:
            todays_forecast_highs[city] = high_temp
        else :
            logging.error('error processing response for ' + entry)

    logging.debug(todays_forecast_highs)

    # Not used here, but just for info
    lowest_city, lowest_high = lowest_high_temp(todays_forecast_highs)

    logging.info('All high temps: ' + str(todays_forecast_highs))
    logging.info('lowest forecast temp is %f celsius in %s' % (lowest_high, lowest_city))

    return todays_forecast_highs


def lowest_high_temp(temps):
    ''' Calculate the smallest temp and corresponding city in a dictionary of { city : temp } pairs '''

    lowest_high = 1000 # Working in Celsius. Unlikely to be any temps above 1000C .... hopefully!
    lowest_city = ''

    for city in temps.keys():
        if temps[city] < lowest_high:
            lowest_high = temps[city]
            lowest_city = city

    if lowest_high == 1000:
        logging.error('The highest low temp is 1000C')

    return lowest_city, lowest_high




#Convenience function for testing this code at the command prompt
def main():
    res = get_forecast_highs()

if __name__ == '__main__':
    main()
