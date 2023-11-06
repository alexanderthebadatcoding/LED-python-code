#!/usr/bin/env python

from samplebase import SampleBase
from rgbmatrix import graphics
import time, random
from datetime import datetime
import yfinance as yf

class StockTicker(SampleBase):
    def __init__(self, *args, **kwargs):
        super(StockTicker, self).__init__(*args, **kwargs)
        self.parser.add_argument("-f", "--font_date", help="Path to font file for date (BDF format)", default="/home/gilby/fonts/lime.bdf")
        self.stocks = ["AAPL", "SPY", "TSLA"]  # List of stock tickers to display

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

        while True:
            offscreen_canvas.Clear()

            # Display stock data
            y_offset = 9  # Adjust the vertical position for stock data

            for ticker in self.stocks:
                stock_data, color = self.fetch_stock_data(ticker)
                graphics.DrawText(offscreen_canvas, font_date, 2, y_offset, color, stock_data)
                y_offset += 9

            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


if __name__ == "__main__":
    stock_ticker = StockTicker()
    if not stock_ticker.process():
        stock_ticker.print_help()

