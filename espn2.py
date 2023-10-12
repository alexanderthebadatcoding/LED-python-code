import time
import sys
import argparse
import requests
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix

# Function to fetch NFL news headlines from the ESPN API
def fetch_nfl_headlines():
    url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/news"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        headlines = [article['headline'] for article in data['articles']]
        return headlines
    else:
        print("Failed to fetch NFL news headlines.")
        return []

# Command-line argument parsing
parser = argparse.ArgumentParser()

parser.add_argument("--led-rows", action="store", help="Display rows. 16 for 16x32, 32 for 32x32. (Default: 32)", default=32, type=int)
parser.add_argument("--led-cols", action="store", help="Panel columns. Typically 32 or 64. (Default: 64)", default=64, type=int)
parser.add_argument("--led-chain", action="store", help="Daisy-chained boards. (Default: 1)", default=1, type=int)
parser.add_argument("--led-parallel", action="store", help="For Plus-models or RPi2: parallel chains. 1..3. (Default: 1)", default=1, type=int)
parser.add_argument("--led-pwm-bits", action="store", help="Bits used for PWM. Range 1..11. (Default: 11)", default=11, type=int)
parser.add_argument("--led-brightness", action="store", help="Sets brightness level. Range: 1..100. (Default: 100)", default=100, type=int)
parser.add_argument("--led-gpio-mapping", help="Hardware Mapping: regular, adafruit-hat, adafruit-hat-pwm" , choices=['regular', 'adafruit-hat', 'adafruit-hat-pwm'], type=str)
parser.add_argument("--led-scan-mode", action="store", help="Progressive or interlaced scan. 0 = Progressive, 1 = Interlaced. (Default: 1)", default=1, choices=range(2), type=int)
parser.add_argument("--led-pwm-lsb-nanoseconds", action="store", help="Base time-unit for the on-time in the lowest significant bit in nanoseconds. (Default: 130)", default=130, type=int)
parser.add_argument("--led-show-refresh", action="store_true", help="Shows the current refresh rate of the LED panel.")
parser.add_argument("--led-slowdown-gpio", action="store", help="Slow down writing to GPIO. Range: 0..4. (Default: 1)", choices=range(5), type=int)
parser.add_argument("--led-no-hardware-pulse", action="store", help="Don't use hardware pin-pulse generation.")
parser.add_argument("--led-rgb-sequence", action="store", help="Switch if your matrix has led colors swapped. (Default: RGB)", default="RGB", type=str)
parser.add_argument("--led-pixel-mapper", action="store", help="Apply pixel mappers. e.g \"Rotate:90\"", default="", type=str)
parser.add_argument("--led-row-addr-type", action="store", help="0 = default; 1 = AB-addressed panels. (Default: 0)", default=0, type=int, choices=[0,1])
parser.add_argument("--led-multiplexing", action="store", help="Multiplexing type: 0 = direct; 1 = strip; 2 = checker; 3 = spiral; 4 = Z-strip; 5 = ZnMirrorZStripe; 6 = coreman; 7 = Kaler2Scan; 8 = ZStripeUneven. (Default: 0)", default=0, type=int)
parser.add_argument("--led-panel-type", action="store", help="Chipset of the panel. In particular if it doesn't light up at all, you might need to play with this option because it indicates that the panel requires a particular initialization sequence.", default="FM6126A", type=str)


args = parser.parse_args()

# Create an RGBMatrix instance
matrix = RGBMatrix(
    rows=args.led_rows,
    cols=args.led_cols,
    chain_length=args.led_chain,
    parallel=args.led_parallel,
    pwm_bits=args.led_pwm_bits,
    brightness=args.led_brightness,
    hardware_mapping=args.led_gpio_mapping
)

# Create an offscreen canvas
offscreen_canvas = matrix.CreateFrameCanvas()

# Fetch NFL news headlines
nfl_headlines = fetch_nfl_headlines()

# Initialize scrolling position
pos = offscreen_canvas.width
headline_index = 0

# Check if there are headlines to display
if nfl_headlines:
    while True:
        offscreen_canvas.Clear()
        font = graphics.Font()
        font.LoadFont("../../../fonts/7x13.bdf")
        textColor = graphics.Color(255, 0, 0)

        # Display the current headline
        current_headline = nfl_headlines[headline_index]
        len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, current_headline)
        pos -= 1

        # Check if the current headline has finished scrolling
        if pos + len < 0:
            pos = offscreen_canvas.width
            headline_index = (headline_index + 1) % len(nfl_headlines)

        # Swap the canvas onto the LED matrix with a delay
        time.sleep(0.05)
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
else:
    print("No NFL headlines to display.")
