import requests
from datetime import datetime

# Replace 'YOUR_API_KEY' with your actual AviationStack API key
api_key = "#"

# AviationStack API endpoint for flight information
endpoint = "http://api.aviationstack.com/v1/flights"

# Specify the parameters for your flight search
params = {
    "access_key": api_key,
    "flight_iata": "WN1499",  # Replace with the flight IATA code you want to retrieve information for
}

# Make the API request
response = requests.get(endpoint, params=params)


# Format Dates
def format_datetime(date_string):
    try:
        parsed_datetime = datetime.fromisoformat(date_string[:-6])
        formatted_datetime = parsed_datetime.strftime("%A, %B %d, %Y %I:%M %p")
        return formatted_datetime
    except ValueError:
        return "Invalid date format"


if response.status_code == 200:
    data = response.json()
    flight_data = data["data"][0]  # Assuming you're interested in the first result

    # Print flight information
    print(f"Flight : {flight_data['flight']['iata']}")
    print(f"Airline: {flight_data['airline']['name']}")
    print(f"Departure Airport: {flight_data['departure']['airport']}")
    print(f"Arrival Airport: {flight_data['arrival']['airport']}")
    print(f"Status: {flight_data['flight_status']}")

    # Check if 'estimated' and 'scheduled' departure times are available
    if (
        "estimated" in flight_data["departure"]
        and "scheduled" in flight_data["departure"]
    ):
        scheduledTime = flight_data["departure"]["scheduled"]
        formatted_sch_time = format_datetime(scheduledTime)
        estimatedTime = flight_data["departure"]["estimated"]
        formatted_est_time = format_datetime(estimatedTime)
        # print(formatted_datetime)
        if formatted_sch_time == formatted_est_time:
            print(f"Scheduled Departure: {formatted_sch_time}")
        else:
            print(f"Estimated Departure: {formatted_est_time}")
        scheduledArrival = flight_data["arrival"]["scheduled"]
        formatted_arrival_time = format_datetime(scheduledArrival)
        estimatedArrival = flight_data["arrival"]["estimated"]
        formatted_est_arr_time = format_datetime(estimatedArrival)
        if formatted_arrival_time == formatted_est_arr_time:
            print(f"Scheduled Arrival: {formatted_arrival_time}")
        else:
            print(f"Estimated Arrival: {formatted_est_arr_time}")


else:
    print(f"Failed to retrieve flight data. Status code: {response.status_code}")
