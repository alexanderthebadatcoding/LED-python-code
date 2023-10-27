from samplebase import SampleBase
from rgbmatrix import graphics
import time, random
from datetime import datetime

class DigitalClock(SampleBase):
    def __init__(self, *args, **kwargs):
        super(DigitalClock, self).__init__(*args, **kwargs)
        # self.parser.add_argument("-f", "--font", help="Path to font file (BDF format)", default="../../../fonts/tom-thumb.bdf")
        self.parser.add_argument("-f_time", "--font_time", help="Path to font file for time (BDF format)", default="/home/gilby/nflscore/matrix/fonts/helvR12.bdf")
        self.parser.add_argument("-f_date", "--font_date", help="Path to font file for date (BDF format)", default="/home/gilby/nflscore/matrix/fonts/tom-thumb.bdf")

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
        font_time = graphics.Font()
        font_time.LoadFont(self.args.font_time)
        font_date = graphics.Font()
        font_date.LoadFont(self.args.font_date)
        textColor = self.get_random_color()
        time_color = self.get_random_color()
        date_color = self.get_random_color()

        while True:
            offscreen_canvas.Clear()
            current_time = time.strftime("%I:%M %p").lstrip("0") # Remove leading zero from hour
            current_day = datetime.now().strftime("%A") # day of the week
            current_date = datetime.now().strftime("%B %d") # Format the date more human-readable

            # Calculate the position to center the time and date text
            graphics.DrawText(offscreen_canvas, font_date, 22, 8, date_color, current_day)
            graphics.DrawText(offscreen_canvas, font_time, 9, 20, time_color, current_time)
            graphics.DrawText(offscreen_canvas, font_date, 13, 28, date_color, current_date)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

    def get_random_color(self):
         return graphics.Color(*map(int, random.choice(self.colors).split(',')))
if __name__ == "__main__":
    digital_clock = DigitalClock()
    if not digital_clock.process():
        digital_clock.print_help()



