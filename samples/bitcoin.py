#!/usr/bin/env python

from samplebase import SampleBase
from rgbmatrix import graphics
import random, requests, locale, time

def get_bitcoin_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin", "vs_currencies": "usd"}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        bitcoin_price = data["bitcoin"]["usd"]

        # Use locale to add commas to the number
        locale.setlocale(locale.LC_ALL, "")  # Set the locale to the system's default

        # Format the price with commas
        formatted_price = locale.format_string("$%.0f", bitcoin_price, grouping=True)
        return formatted_price
    else:
        return None

bitcoin_price = get_bitcoin_price()
bitcoin_symbol = "\u20BF"  # Unicode character for the Bitcoin symbol (₿)
# print(f"Bitcoin Symbol: {bitcoin_symbol}")
if bitcoin_price is not None:
    print(f"{bitcoin_symbol} {bitcoin_price}")
else:
    print("Failed to retrieve Bitcoin price.")


class BitcoinDisplay(SampleBase):
    def __init__(self, *args, **kwargs):
        super(BitcoinDisplay, self).__init__(*args, **kwargs)
        self.parser.add_argument("-f_text", "--font_text", help="Path to font file for date (BDF format)", default="/home/gilby/fonts/cherry.bdf")
        self.parser.add_argument("-f_num", "--font_num", help="Path to font file for date (BDF format)", default="/home/gilby/fonts/timB14.bdf")
        self.parser.add_argument("--led-pwm-dither-bits", action="store", help="", default=2, type=int)
        self.parser.add_argument("--led-pwm-lsb-nanoseconds=250")
        self.parser.add_argument("--led-slowdown-gpio=2")

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font_text = graphics.Font()
        font_text.LoadFont(self.args.font_text)
        font_num = graphics.Font()
        font_num.LoadFont(self.args.font_num)
        text_color = graphics.Color(255, 155, 0)
        btc_color = graphics.Color(255, 255, 255)
        bitcoin_price = get_bitcoin_price()

        while True:
            offscreen_canvas.Clear()
            graphics.DrawText(offscreen_canvas, font_text, 7, 12, btc_color, "Bitcoin")
            graphics.DrawText(offscreen_canvas, font_num, 3, 28, text_color, bitcoin_price)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            time.sleep(5)
            bitcoin_price = get_bitcoin_price()


if __name__ == "__main__" :
    bitcoin_display = BitcoinDisplay()
    if not bitcoin_display.process():
        bitcoin_display.print_help()
