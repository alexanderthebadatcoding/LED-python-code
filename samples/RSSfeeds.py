from samplebase import SampleBase
from rgbmatrix import graphics
import time
import feedparser
import random
import sys

class RSSFeedDisplay(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RSSFeedDisplay, self).__init__(*args, **kwargs)
        self.parser.add_argument("--led-pwm-dither-bits", action="store", help="", default=2, type=int)
        self.parser.add_argument("--led-pwm-lsb-nanoseconds=100")
        self.parser.add_argument("-f", "--font", help="Path to font file (BDF format)", default="/home/gilby/fonts/win_crox3h.bdf")
        self.parser.add_argument("-n", "--num_items", type=int, help="Number of items to display", default=11)
        self.parser.add_argument("-s", "--scroll_speed", type=float, help="Scroll speed in pixels per frame", default=2.0)  # Added scroll_speed argument
        self.feeds = [
            "https://www.espn.com/espn/rss/news",
            "https://www.espn.com/espn/rss/nfl/news",
            "https://www.espn.com/blog/feed?blog=nflnation",
            "https://www.espn.com/espn/rss/soccer/news",
            "https://www.espn.com/espn/rss/ncf/news",
            "https://api.foxsports.com/v2/content/optimized-rss?partnerKey=MB0Wehpmuj2lUhuRhQaafhBjAJqaPU244mlTDK1i&size=30&tags=fs/nfl",
            "https://seekingalpha.com/market_currents.xml",
            "https://www.investing.com/rss/news.rss",
            "https://www.techrepublic.com/rssfeeds/articles/",
            "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
            "https://sports.yahoo.com/rss/",
            "https://www.techradar.com/rss/news/gaming",
            "https://www.techradar.com/rss",
            "http://www.cnbc.com/id/19746125/device/rss/rss.xml",
            "http://america.aljazeera.com/content/ajam/articles.rss",
            "https://news.bitcoin.com/feed/",
            "http://www.npr.org/rss/rss.php?id=1001",
            "https://www.rotowire.com/rss/news.php?sport=NFL",
            "https://www.draftsharks.com/rss/shark-bites",
            "https://www.draftsharks.com/rss/latest-news",
            "http://feeds.marketwatch.com/marketwatch/topstories/",
            "http://feeds.marketwatch.com/marketwatch/StockstoWatch/"
        ]
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
        scroll_speed = self.args.scroll_speed

        while True:
            offscreen_canvas.Clear()
            # Shuffle the feed URLs to display them in random order
            random.shuffle(self.feeds)
            textColor = self.get_random_color()
            for feed_url in self.feeds:
                feed = feedparser.parse(feed_url)
                #print(feed_url)
                items = feed.entries[:self.args.num_items]
                random.shuffle(items)

                if not items:
                    # If no items are available for the feed, display a message
                    message = "No RSS items found for this feed."
                    len_message = graphics.DrawText(offscreen_canvas, font, 1, 22, textColor, message)
                    time.sleep(2)
                else:
                    # Display RSS feed items as scrolling text with random colors
                    for item in items:
                        item_title = item.title
                        textColor = self.get_random_color()
                        len_title = graphics.DrawText(offscreen_canvas, font, offscreen_canvas.width, 0, textColor, item_title)
                        pos = offscreen_canvas.width

                        while pos + len_title > 0:
                            offscreen_canvas.Clear()
                            pos -= scroll_speed
                            len_title = graphics.DrawText(offscreen_canvas, font, pos, 20, textColor, item_title)
                            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
                            time.sleep(0.02)
                    print("Done")
                    sys.exit(0)

    def get_random_color(self):
         return graphics.Color(*map(int, random.choice(self.colors).split(',')))

if __name__ == "__main__":
    rss_feed_display = RSSFeedDisplay()
    if not rss_feed_display.process():
        rss_feed_display.print_help()

