'''various human tidying was needed after running this file. Data set contained
data like 'Jersey, NJ', which WU doesn't interpret as 'Jersey City'. Same for 'Oklahoma City' and various others  '''

with open('cities.txt', 'r') as f:
    lines = f.readlines()

cities = [ line.replace(',', ';').strip() for line in lines if line[0].isalpha() ]

#print(cities)

state_abbr = {}


with open('state_abbr.txt', 'r') as f:
    state_abbr = { line.split('\t')[0] : line.split('\t')[1].strip() for line in f.readlines() }
    #print(state_abbr)

# replace state with abbreviation

city_abbr = []

for city in cities:
    # cities contains strings 'North Las Vegas; Nevada'
    print(city)
    state = city.split('; ')[1]

    city_name = city.split('; ')[0]
    # remove anything after a / or a -
    if '/' in city_name:
        city_name = city_name[0 : city_name.find('/')]  # Sorry Jefferson KY

    if '-' in city_name:
        city_name = city_name[0 : city_name.find('-')]  # Sorry Davidson TN  (But Winston-Salem NC needs to stay hyphenated)

    try:
        abbr = state_abbr[state]
        # Replace the LAST instance only ! Or Oklahoma City gets turned into OK City
        city = city_name + '; ' + abbr
        city_abbr.append(city)

    except KeyError:
        if state not in state_abbr.values():
            print('warning state not found?')
            print(city)

print(city_abbr)




with open('city_data.txt', 'w') as f:
    for city in city_abbr:
        f.write(city + '\n')
