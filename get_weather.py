from keys import keys
from time import sleep
import urllib2
import logging

import json
import os

sleepdelay = 70
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
    ### TODO key error !!
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

    # Get smallest val from todays_forecast_highs

    lowest = 100 # Working in Celsius. Unlikely to be any temps above the boiling point of water (hopefully)
    lowest_city = ''

    logging.debug(todays_forecast_highs)

    for city in todays_forecast_highs.keys():
        if todays_forecast_highs[city] < lowest:
            lowest = todays_forecast_highs[city]
            lowest_city = entry


    logging.info('All high temps: ' + str(todays_forecast_highs)
    logging.info('lowest forecast temp is %f in %s' % (lowest, lowest_city))

    return todays_forecast_highs


def main():
    res = get_forecast_highs()

if __name__ == '__main__':
    main()
