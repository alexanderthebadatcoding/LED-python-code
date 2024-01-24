import requests
import pytz
from datetime import datetime


# API endpoint URL
api_url = "https://external.transitapp.com/v3/public/stop_departures"
# API key for authentication
api_key = 'api_key'  # Make sure to replace with your actual API key

# Set up headers with the API key
headers = {
    'apiKey': api_key,
}

# List of global stop IDs
stop_ids = ['KCATA:40812', 'KCATA:40756'] # replace with relevant stops

for stop_id in stop_ids:
    # Parameters for the request
    params = {
        'lat': 39.0337542,
        'lon': -94.5727608,
        'global_stop_id': stop_id,
        'should_update_realtime': 'true' 
    }
    # Make the GET request with headers
    response = requests.get(api_url, params=params, headers=headers)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse and use the response data
        data = response.json()
        #print(data)
        dept_time = data['route_departures'][0]['itineraries'][0]['schedule_items'][0]['departure_time']
        utc_departure_datetime = datetime.utcfromtimestamp(dept_time)
        central_timezone = pytz.timezone('America/Chicago')
        central_departure_datetime = utc_departure_datetime.replace(tzinfo=pytz.utc).astimezone(central_timezone)
        formatted_departure_time = central_departure_datetime.strftime('%I:%M %p')
        # Accessing and printing 'headsign' and 'route_long_name'
        headsign = data['route_departures'][0]['itineraries'][0]['headsign']
        route_long_name = data['route_departures'][0]['route_long_name']  
        print(f"{route_long_name} {headsign} at {formatted_departure_time}")
        #print(departure_datetime)
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code} - {response.text}")
