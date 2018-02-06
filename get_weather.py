from keys import keys
from time import sleep
import urllib2
import logging
logging.getLogger().setLevel(logging.DEBUG)

import json
import os

key = keys['WEATHER_UNDERGROUND']

city_list_file = os.path.join('data', 'city_data.txt')

sleep_delay = 60

url_base = 'http://api.wunderground.com/api/%s/forecast/q/%s/%s.json'


def get_weather(url):

    try:
        response = urllib2.urlopen(url)
        text = response.read()
        json_response = json.loads(text)
        return json_response
    except Exception as e:
        logging.error('Error fetching data from ' + url + " error: " + str(e))
        return None


def get_high(response):
    """ get the high temp from the json
    :param response: JSON response from WU  """
    try:
        high = response["forecast"]["simpleforecast"]["forecastday"][0]['high']['celsius']
        return float(high)
    except Exception as e:
        logging.warning('Error reading the following JSON ' + str(response) + 'error: ' + str(e))
        return None


def get_forecast_highs():

    with open(city_list_file, 'r') as f:
        cities = f.readlines()

    rate_limiter = 0
    today_forecast_highs = {}

    for entry in cities:

        logging.info('Query %d fetching data for %s' % (rate_limiter, entry))

        city = entry.split('; ')[0].replace(' ', '_')
        state = entry.split('; ')[1].strip()

        url = url_base % (key, state, city)

        resp = get_weather(url)
        if resp:
            high_temp = get_high(resp)
            if high_temp:
                today_forecast_highs[city] = high_temp

        rate_limiter += 1
        if rate_limiter % 10 == 0 and rate_limiter % len(cities) != 0:
            logging.info('sleeping for %s seconds' % sleep_delay)
            sleep(sleep_delay)


    logging.debug(today_forecast_highs)

    # Not used here, but just for info
    lowest_city, lowest_high = lowest_high_temp(today_forecast_highs)

    logging.info('All high temps: ' + str(today_forecast_highs))
    logging.info('lowest forecast temp is %f celsius in %s' % (lowest_high, lowest_city))

    return today_forecast_highs


def lowest_high_temp(temps):
    """ :param temps: dictionary of { city : temp } pairs
    Identify and return the lowest temp and associated city. Returns None, None if
    """

    lowest_high = 1000  # Working in Celsius. Unlikely to be any temps above 1000C .... hopefully!
    lowest_city = ''

    for city, temp in temps.items():
        if temp < lowest_high:
            lowest_high = temp
            lowest_city = city

    if lowest_high == 1000:
        logging.error('Error identifying highest temp in JSON ' + str(temps))
        return None, None

    return lowest_city, lowest_high


#Convenience function for testing this code at the command prompt
if __name__ == '__main__':
    res = get_forecast_highs()
    print(res)


