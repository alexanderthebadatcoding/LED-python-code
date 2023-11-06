#!/usr/bin/env python

from samplebase import SampleBase
from rgbmatrix import graphics
import time, random
from datetime import datetime
import yfinance as yf

# Number of stocks to select at a time
batch_size = 3

# Delay in seconds
delay = 30

class StockTicker(SampleBase):
    def __init__(self, *args, **kwargs):
        super(StockTicker, self).__init__(*args, **kwargs)
        self.parser.add_argument("-f", "--font_date", help="Path to font file for date (BDF format)", default="/home/gilby/fonts/lime.bdf")
        self.parser.add_argument("-loading", "--loading_font", help="Path to font", default="/home/gilby/fonts/simpl.bdf")
        self.parser.add_argument("--led-pwm-lsb-nanoseconds=250")
        self.parser.add_argument("--led-slowdown-gpio=1")
        self.stocks = ["AAPL", "SPY", "TSLA", "ROKU", "PYPL", "AMZN", "MSFT", "CEI", "NFLX", "NVDA", "PSEC", "AAL", "AMD", "INTC", "IBM", "CSCO", "BOTZ", "CNSL", "PLUG", "UUUU", "F", "GM"]
        random.shuffle(self.stocks)
        self.selected_stocks = self.stocks[:3]
        print(self.selected_stocks)

    def fetch_stock_data(self, ticker):
        try:
            stock_data = yf.Ticker(ticker)
            price = stock_data.history(period="1d")['Close'].iloc[0]
            previous_close = stock_data.history(period="1d")['Close'].iloc[-1]

            if price > previous_close:
                color = graphics.Color(0, 255, 0)  # Green
            elif price < previous_close:
                color = graphics.Color(255, 0, 0)  # Red
            else:
                color = graphics.Color(255, 255, 255)  # White (No price change)

            return (f"{ticker}: {price:.2f}", color)
        except Exception as e:
            return (f"{ticker}: Error fetching data", graphics.Color(255, 255, 255))

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font_date = graphics.Font()
        font_date.LoadFont(self.args.font_date)
        loading_font = graphics.Font()
        loading_font.LoadFont(self.args.loading_font)

        white = graphics.Color(255, 255, 255)
        graphics.DrawText(offscreen_canvas, loading_font, 15, 17, white, "Loading...")
        # Display the canvas for 3 seconds
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
        # time.sleep(2)

        while True:
            offscreen_canvas.Clear()

            # Display stock data
            y_offset = 9  # Adjust the vertical position for stock data

            for ticker in self.selected_stocks:
                stock_data, color = self.fetch_stock_data(ticker)
                # print(stock_data)
                graphics.DrawText(offscreen_canvas, font_date, 2, y_offset, color, stock_data)
                y_offset += 9

            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


if __name__ == "__main__":
    stock_ticker = StockTicker()
    if not stock_ticker.process():
        stock_ticker.print_help()

