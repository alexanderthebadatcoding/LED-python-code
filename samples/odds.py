#!/usr/bin/env python

from samplebase import SampleBase
from rgbmatrix import graphics
import time, random, sys
import requests
from datetime import datetime
import pytz

class RSSFeedDisplay(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RSSFeedDisplay, self).__init__(*args, **kwargs)
        self.parser.add_argument("-f", "--font", help="Path to font file (BDF format)", default="/home/gilby/nflscore/matrix/fonts/9x18.bdf")
        self.parser.add_argument("--led-pwm-dither-bits", action="store", help="", default=2, type=int)
        self.parser.add_argument("--led-pwm-lsb-nanoseconds=250")
        self.parser.add_argument("--led-slowdown-gpio=2")
        self.colors = [
            "189,51,164",  # byzantine
            "252,194,0",   # golden poppy
            "56,189,248",  # cyan
            "252,211,77",  # yellow gold
            "128,0,128",   # purple
            "255,165,0",   # orange
            "0,0,255",     # blue
            "128,128,0",   # olive
            "242,178,244",
            "147,201,200",
            "224,169,170",
            "200,147,201",
            "148,201,147",
            "195,226,255"
        ]

    def fetch_odds_data(self):
        # Update with Your API Key
        base_url = "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/?regions=us&oddsFormat=american&apiKey=APIKEY"

        response = requests.get(base_url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont(self.args.font)

        while True:
            offscreen_canvas.Clear()
            textColor = self.get_random_color()
            # Fetch and parse the odds data
            odds_data = self.fetch_odds_data()
            if odds_data:
                for event in odds_data:
                    event_name = f'{event["home_team"]} vs. {event["away_team"]}'
                    outcomes = event["bookmakers"][0]["markets"][0]["outcomes"]
                    # outcome_data = ", ".join([f'{outcome["name"]}: {outcome["price"]}' for outcome in outcomes])
                    # event_data = f"{event_name}: {outcome_data}"
                    outcome_data = ", ".join([f'{outcome["name"]}: {outcome["price"]}' for outcome in outcomes])
                    event_data = f"{outcome_data}"
                    len_title = graphics.DrawText(offscreen_canvas, font, offscreen_canvas.width, 12, textColor, event_data)
                    pos = offscreen_canvas.width
                    textColor = self.get_random_color()

                    while pos + len_title > 0:
                        offscreen_canvas.Clear()
                        pos -= 2
                        len_title = graphics.DrawText(offscreen_canvas, font, pos, 22, textColor, event_data)
                        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
                        time.sleep(0.02)

            sys.exit(0)

    def get_random_color(self):
        return graphics.Color(*map(int, random.choice(self.colors).split(',')))

if __name__ == "__main__":
    rss_feed_display = RSSFeedDisplay()
    if not rss_feed_display.process():
        rss_feed_display.print_help()

