import requests
import time
from datetime import datetime
from rgbmatrix import RGBMatrix, RGBMatrixOptions

# Set up the RGB LED matrix
options = RGBMatrixOptions()
options.hardware_mapping = "adafruit-hat-pwm"  # Check your hardware mapping
matrix = RGBMatrix(options=options)

# Weather API configuration
api_key = "YOUR_API_KEY"
city = "YourCity"
weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

while True:
    # Get weather data
    response = requests.get(weather_url)
    if response.status_code == 200:
        weather_data = response.json()
        temperature = weather_data["main"]["temp"]
        weather_description = weather_data["weather"][0]["description"]
    else:
        temperature = "N/A"
        weather_description = "N/A"

    # Get current time
    current_time = datetime.now().strftime("%H:%M:%S")

    # Display weather and time on the LED matrix
    matrix.Clear()
    matrix.DrawText(0, 16, matrix.Color(255, 255, 255), f"Temperature: {temperature}°C")
    matrix.DrawText(
        0, 32, matrix.Color(255, 255, 255), f"Weather: {weather_description}"
    )
    matrix.DrawText(0, 48, matrix.Color(255, 255, 255), f"Time: {current_time}")
    time.sleep(300)  # Update every 5 minutes
