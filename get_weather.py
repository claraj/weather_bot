from keys import keys
from time import sleep
#import requests
import urllib2

import json
import os

sleepdelay = 70
key = keys['WEATHER_UNDERGROUND']

city_list_file = os.path.join('data', 'city_data_tmp.txt')

url_base = 'http://api.wunderground.com/api/%s/forecast/q/%s/%s.json'

def get_weather(url, city, state):

    #response = requests.get(url)
    #json_response = response.json()  # Make a dictionary

    response = urllib2.urlopen(url)
    text = response.read()
    json_response = json.loads(text)

    # filename = os.path.join('out', city + '_' + state + '.json')
    # with open(filename, 'w') as f:
    #     f.write(json.dumps(json_response))

    return json_response

def get_high(response):
    ''' get the high temp from the json'''
    ### TODO key error !!
    try:
        high = response["forecast"]["simpleforecast"]["forecastday"][0]['high']['celsius']
        return float(high)
    except KeyError:
        return None


def get_forecast_highs():

    with open(city_list_file, 'r') as f:
        cities = f.readlines()

    rate_limiter = 0

    todays_forecast_highs = {}

    for entry in cities:

        rate_limiter += 1

        print('Query %d fetching data for %s' % (rate_limiter, entry))

        if rate_limiter % 10 == 0:
            print('sleeping')
            sleep(sleepdelay)

        city = entry.split('; ')[0].replace(' ', '_')
        state = entry.split('; ')[1].strip()

        url = url_base % ( key, state, city)

        resp = get_weather(url, city, state)
        high_temp = get_high(resp)

        if high_temp is not None:
            todays_forecast_highs[city] = high_temp
        else :
            print('error processing response for ' + entry)

    # Get smallest val from todays_forecast_highs

    lowest = 100 # Working in Celsius. Unlikely to be any temps above the boiling point of water (hopefully)
    lowest_city = ''

    print(todays_forecast_highs)

    for city in todays_forecast_highs.keys():
        if todays_forecast_highs[city] < lowest:
            lowest = todays_forecast_highs[city]
            lowest_city = entry

    print('lowest forecast temp is %f in %s' % (lowest, lowest_city))

    # with open(os.path.join('out', 'summary.txt'), 'w') as f:
    #     f.write(str(todays_forecast_highs))

    return todays_forecast_highs


def main():
    res = get_forecast_highs()
    print(res)

if __name__ == '__main__':
    main()
