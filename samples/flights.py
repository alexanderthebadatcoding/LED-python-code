from samplebase import SampleBase
from rgbmatrix import graphics
import time, random, sys
import requests
from datetime import datetime
import pytz


class FlightDisplay(SampleBase):
    def __init__(self, *args, **kwargs):
        super(FlightDisplay, self).__init__(*args, **kwargs)
        self.parser.add_argument(
            "-f",
            "--font",
            help="Path to font file (BDF format)",
            default="/home/pi/nflscore/matrix/fonts/9x18.bdf",
        )
        self.parser.add_argument(
            "-info", "--info", help="Pick Flight Number to show", default="WN1499"
        )
        self.parser.add_argument(
            "--led-pwm-dither-bits", action="store", help="", default=2, type=int
        )
        self.parser.add_argument("--led-pwm-lsb-nanoseconds=250")
        self.parser.add_argument("--led-slowdown-gpio=2")

    # Format Dates
    def format_datetime(self, date_string):
        try:
            parsed_datetime = datetime.fromisoformat(date_string[:-6])
            formatted_datetime = parsed_datetime.strftime("%A, %B %d, %Y %I:%M %p")
            return formatted_datetime
        except ValueError:
            return "Invalid date format"

    def get_flight_information(self, flight_data):
        formatted_info = ""

        # Check if 'estimated' and 'scheduled' departure times are available
        if "departure" in flight_data:
            departure_data = flight_data["departure"]
            if "scheduled" in departure_data and "estimated" in departure_data:
                scheduledTime = departure_data["scheduled"]
                estimatedTime = departure_data["estimated"]

                try:
                    formatted_sch_time = self.format_datetime(scheduledTime)
                    formatted_est_time = self.format_datetime(estimatedTime)

                    if formatted_sch_time == formatted_est_time:
                        formatted_info += f"Scheduled Departure: {formatted_sch_time}, "
                    else:
                        formatted_info += f"Estimated Departure: {formatted_est_time}, "
                except ValueError:
                    formatted_info += "Error formatting departure times"

        # Check if 'estimated' and 'scheduled' arrival times are available
        if "arrival" in flight_data:
            arrival_data = flight_data["arrival"]
            if "scheduled" in arrival_data and "estimated" in arrival_data:
                scheduledArrival = arrival_data["scheduled"]
                estimatedArrival = arrival_data["estimated"]

                try:
                    formatted_arrival_time = self.format_datetime(scheduledArrival)
                    formatted_est_arr_time = self.format_datetime(estimatedArrival)

                    if formatted_arrival_time == formatted_est_arr_time:
                        formatted_info += f"Scheduled Arrival: {formatted_arrival_time}"
                    else:
                        formatted_info += f"Estimated Arrival: {formatted_est_arr_time}"
                except ValueError:
                    formatted_info += "Error formatting arrival times"
        # print(formatted_info)
        return formatted_info

    def fetch_flight_data(self):
        # Replace 'YOUR_API_KEY' with your actual AviationStack API key
        api_key = "api_key"

        # AviationStack API endpoint for flight information
        endpoint = "http://api.aviationstack.com/v1/flights"

        # Specify the parameters for your flight search
        params = {
            "access_key": api_key,
            "flight_iata": self.args.info,  # Replace with the flight IATA code you want to retrieve information for
        }

        # Make the API request
        response = requests.get(endpoint, params=params)

        if response.status_code == 200:
            data = response.json()
            flight_data = data["data"][
                0
            ]  # Assuming you're interested in the first result
            return flight_data

        else:
            offscreen_canvas = self.matrix.CreateFrameCanvas()
            font = graphics.Font()
            font.LoadFont(self.args.font)
            offscreen_canvas.Clear()
            textColor = graphics.Color(255, 255, 255)
            print(
                f"Failed to retrieve flight data. Status code: {response.status_code}"
            )
            graphics.DrawText(
                offscreen_canvas, font, 2, 22, textColor, "error connecting"
            )
            return None

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont(self.args.font)

        while True:
            offscreen_canvas.Clear()
            textColor = graphics.Color(255, 255, 255)
            # Fetch and parse the odds data
            flight_data = self.fetch_flight_data()
            formatted_flight_info = self.get_flight_information(flight_data)
            # if flight_data:
            # for event in flight_data:
            flight = f"{flight_data['flight']['iata']}"
            airline = f"{flight_data['airline']['name']}"
            dep_airport = f"{flight_data['departure']['airport']}"
            arr_airport = f"{flight_data['arrival']['airport']}"
            status = f"Status: {flight_data['flight_status']}"
            flight_times = f"{formatted_flight_info}"
            event_info = f"{airline} {flight}: {dep_airport} to {arr_airport}, {flight_times}, {status}"
            len_title = graphics.DrawText(
                offscreen_canvas,
                font,
                offscreen_canvas.width,
                22,
                textColor,
                event_info,
            )
            pos = offscreen_canvas.width

            while pos + len_title > 0:
                offscreen_canvas.Clear()
                pos -= 2
                len_title = graphics.DrawText(
                    offscreen_canvas, font, pos, 22, textColor, event_info
                )
                offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
                time.sleep(0.02)

            sys.exit(0)


if __name__ == "__main__":
    flight_display = FlightDisplay()
    if not flight_display.process():
        flight_display.print_help()
