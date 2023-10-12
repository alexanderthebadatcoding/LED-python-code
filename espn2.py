import time
import sys
import argparse
import requests
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix

# Function to fetch news results from the ESPN API
def fetch_news_results():
    url = "https://site.api.espn.com/apis/site/v2/search"
    params = {
        "query": "news",
        "limit": 5,  # You can adjust the number of results to fetch
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        return results
    else:
        print("Failed to fetch news results.")
        return []

# Command-line argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("--led-rows", type=int, default=32, help="Number of rows in your RGB LED matrix")
parser.add_argument("--led-cols", type=int, default=64, help="Number of columns in your RGB LED matrix")
parser.add_argument("--led-chain", type=int, default=1, help="Number of daisy-chained panels")
parser.add_argument("--led-parallel", type=int, default=1, help="Number of parallel chains")
parser.add_argument("--led-pwm-bits", type=int, default=11, help="Bits used for PWM")
parser.add_argument("--led-brightness", type=int, default=100, help="Brightness (0-100)")
parser.add_argument("--led-parallel-map", type=str, default="default", help="Parallel pixel mapping")
parser.add_argument("--led-gpio-mapping", type=str, default="regular", help="GPIO mapping")
args = parser.parse_args()

# Create an RGBMatrix instance
matrix = RGBMatrix(
    rows=args.led_rows,
    cols=args.led_cols,
    chain_length=args.led_chain,
    parallel=args.led_parallel,
    pwm_bits=args.led_pwm_bits,
    brightness=args.led_brightness,
    hardware_mapping=args.led_gpio_mapping,
    parallel_map=args.led_parallel_map
)

# Create an offscreen canvas
offscreen_canvas = matrix.CreateFrameCanvas()

# Fetch news results
news_results = fetch_news_results()

# Initialize scrolling position
pos = offscreen_canvas.width
result_index = 0

# Check if there are news results to display
if news_results:
    while True:
        offscreen_canvas.Clear()
        font = graphics.Font()
        font.LoadFont("/fonts/7x13.bdf")
        textColor = graphics.Color(255, 0, 0)

        # Display the current news result
        current_result = news_results[result_index]
        headline = current_result.get('title', 'No Title')
        description = current_result.get('description', 'No Description')
        text = f"{headline} - {description}"
        len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, text)
        pos -= 1

        # Check if the current news result has finished scrolling
        if pos + len < 0:
            pos = offscreen_canvas.width
            result_index = (result_index + 1) % len(news_results)

        # Swap the canvas onto the LED matrix with a delay
        time.sleep(0.05)
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
else:
    print("No news results to display.")
