import time
from samplebase import SampleBase
from rgbmatrix import graphics

class StockTicker(SampleBase):
    def __init__(self, *args, **kwargs):
        super(StockTicker, self).__init__(*args, **kwargs)
        self.parser.add_argument("--stocks", nargs="+", help="List of stock tickers to display", default=["AAPL", "GOOGL", "TSLA"])
        self.stocks_data = {}  # A dictionary to store stock data

    def fetch_stock_data(self, ticker):
        # Replace this with your code to fetch stock data for the given ticker from your data source or API
        # Example: You can use a library like 'yfinance' to fetch stock data
        # Import and use 'yfinance' to retrieve stock data
        # import yfinance as yf
        # stock_data = yf.Ticker(ticker)
        # price = stock_data.history(period="1d")['Close'].iloc[0]
        # return f"{ticker}: {price}"

        # For the sake of the example, let's simulate stock data
        import random
        price = random.uniform(100, 200)
        return f"{ticker}: ${price:.2f}"

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("../../../fonts/7x13.bdf")
        textColor = graphics.Color(255, 255, 0)

        while True:
            offscreen_canvas.Clear()
            x = offscreen_canvas.width

            for ticker in self.stocks_data:
                text = self.stocks_data[ticker]
                len_text = graphics.TextWidth(font, text)
                len_ticker = graphics.TextWidth(font, ticker)
                graphics.DrawText(offscreen_canvas, font, x, 10, textColor, ticker)
                x += len_ticker
                x += 5
                graphics.DrawText(offscreen_canvas, font, x, 10, textColor, text)
                x += len_text + 10

            # Fetch and update stock data
            for ticker in self.parser.stocks:
                self.stocks_data[ticker] = self.fetch_stock_data(ticker)

            x -= 1
            if x < 0:
                x = offscreen_canvas.width

            time.sleep(1)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

if __name__ == "__main__":
    stock_ticker = StockTicker()
    if not stock_ticker.process():
        stock_ticker.print_help()
