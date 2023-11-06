#!/usr/bin/env python

from samplebase import SampleBase
from rgbmatrix import graphics
import time
import feedparser
import random

class RSSFeedDisplay(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RSSFeedDisplay, self).__init__(*args, **kwargs)
        self.parser.add_argument("-f", "--font", help="Path to font file (BDF format)", default="/home/gilby/nflscore/matrix/fonts/9x18.bdf")
        self.parser.add_argument("-u", "--url", help="URL of the RSS feed", required=True)
        self.parser.add_argument("-n", "--num_items", type=int, help="Number of items to display", default=8)
        self.colors = [
            "189,51,164", # byzantine
            "252,194,0",  # golden poppy
            "56,189,248",  # cyan
            "252,211,77",  # yellow gold
            "128,0,128",   # purple
            "255,165,0",   # orange
            "0,0,255",     # blue
            "128,128,0",    # olive
            "242,178,244",
            "147,201,200",
            "224,169,170",
            "200,147,201",
            "148,201,147",
            "195,226,255"
        ]

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont(self.args.font)
        textColor = self.get_random_color()

        while True:
            offscreen_canvas.Clear()

            # Fetch and parse the RSS feed
            feed = feedparser.parse(self.args.url)
            items = feed.entries[:self.args.num_items]
            random.shuffle(items)

            if not items:
                # If no items are available, display a message
                message = "No RSS items found."
                len_message = graphics.DrawText(offscreen_canvas, font, 1, 12, textColor, message)
                time.sleep(2)
            else:
                # Display RSS feed items as scrolling text
                for item in items:
                    item_title = item.title
                    textColor = self.get_random_color()
                    len_title = graphics.DrawText(offscreen_canvas, font, offscreen_canvas.width, 12, self.get_random_color(), item_title)
                    pos = offscreen_canvas.width

                    while pos + len_title > 0:
                        offscreen_canvas.Clear()
                        pos -= 1.8
                        len_title = graphics.DrawText(offscreen_canvas, font, pos, 22, textColor, item_title)
                        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
                        time.sleep(0.02)

    def get_random_color(self):
         return graphics.Color(*map(int, random.choice(self.colors).split(',')))


if __name__ == "__main__":
    rss_feed_display = RSSFeedDisplay()
    if not rss_feed_display.process():
        rss_feed_display.print_help()

