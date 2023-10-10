import requests
import time
from PIL import Image, ImageDraw, ImageFont
from rgbmatrix import RGBMatrix, RGBMatrixOptions

# Set up the RGB LED matrix
options = RGBMatrixOptions()
options.hardware_mapping = "adafruit-hat-pwm"  # Check your hardware mapping
matrix = RGBMatrix(options=options)

# Define the ESPN API URL
url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/news?limit=50"

while True:
    # Make an API request to ESPN
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Extract and display news on the LED matrix
        # Replace this part with your code to display news on the matrix
        news_headlines = [article["headline"] for article in data.get("articles", [])]
        for headline in news_headlines:
            matrix.Clear()
            matrix.DrawText(0, 16, matrix.Color(255, 255, 255), headline)
            time.sleep(5)  # Display each headline for 5 seconds
    else:
        print(f"Error: {response.status_code}")
    time.sleep(300)  # Fetch news every 5 minutes
