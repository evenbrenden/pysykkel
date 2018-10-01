import requests
import argparse
import json
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--client-identifier', help='Client Identifier', required=True)
args = parser.parse_args()

try:
    stations_url = 'https://oslobysykkel.no/api/v1/stations'
    availability_url = 'https://oslobysykkel.no/api/v1/stations/availability'
    headers = {'Client-Identifier': args.client_identifier}
    stations_response = requests.get(stations_url, headers=headers)
    availability_response = requests.get(availability_url, headers=headers)
except RequestException:
    print('Something went wrong')
    sys.exit(0)

try:
    stations = json.loads(stations_response.text)
    availabilities = json.loads(availability_response.text)
except JSONDecodeError:
    print('Something went wrong')
    sys.exit(0)

if 'error' in stations:
    print(stations['error'])
    sys.exit(0)

try:
    merged = [{**x, **y} for x in stations['stations'] for y in availabilities['stations'] if x['id'] == y['id']]
    for station in merged:
        title = station['title']
        subtitle = station['subtitle']
        availability = station['availability']
        bikes = availability['bikes']
        locks = availability['locks']
        print(title + ' ' + subtitle + ' has ' + str(bikes) +  ' available bikes and ' + str(locks) + ' available locks.')
except KeyError:
    print('Something went wrong')

