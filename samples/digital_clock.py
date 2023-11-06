#!/usr/bin/env python

from samplebase import SampleBase
from rgbmatrix import graphics
import time, random
from datetime import datetime

class DigitalClock(SampleBase):
    def __init__(self, *args, **kwargs):
        super(DigitalClock, self).__init__(*args, **kwargs)
        # self.parser.add_argument("-f", "--font", help="Path to font file (BDF format)", default="../../../fonts/tom-thumb.bdf")
        self.parser.add_argument("-f_time", "--font_time", help="Path to font file for time (BDF format)", default="/home/gilby/fonts/aqui.bdf")
        self.parser.add_argument("-f_date", "--font_date", help="Path to font file for date (BDF format)", default="/home/gilby/fonts/lime.bdf")
        self.parser.add_argument("--led-slowdown-gpio=2")

        self.colors = [
            "189,51,164", # byzantine
            "255,128,73",  # golden poppy
            "56,189,248",  # cyan
            "252,211,77",  # yellow gold
            "255,165,0",   # orange
            "100,10,255",     # blue
            "64,0,128",
            "242,178,244",
            "224,169,170",
            "20,147,201",
            "148,201,147",
            "195,226,255",
            "88,104,120",
            "255,239,189",
            "173,154,238",
            "84,84,84"
        ]

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font_time = graphics.Font()
        font_time.LoadFont(self.args.font_time)
        font_date = graphics.Font()
        font_date.LoadFont(self.args.font_date)
        # time_color = self.get_random_color()
        random.shuffle(self.colors)
        # Get the first color string from the list
        first_color_string = self.colors[0]
        second_color_string = self.colors[2]
        print(first_color_string, second_color_string)
        if first_color_string == second_color_string:
            random.shuffle(self.colors)
        # Split the string into individual RGB values
        r, g, b = map(int, first_color_string.split(','))
        r2, g2, b2 = map(int, second_color_string.split(','))
        # Create an rgbmatrix.graphics.Color object
        time_color = graphics.Color(r, g, b)

        date_color = graphics.Color(r2, g2, b2)

        while True:
            offscreen_canvas.Clear()
            current_time = time.strftime("%I:%M").lstrip("0") # Remove leading zero from hour
            am_pm = time.strftime("%p")
            current_day = datetime.now().strftime("%A") # day of the week
            current_date = datetime.now().strftime("%B %d") # Format the date more human-readable

            # Calculate the position to center the time and date text
            # Estimate the text width
            time_width = len(current_time) // 2
            time_padding = len(current_time) * 7
            # print(len(current_time))
            date_width = len(current_date) * 4.7
            day_width = len(current_day) * 4.56

            # print(datetime.now().hour)
            # Fix padding based on time
            if datetime.now().hour in [10, 11, 12]:
               offsetx = 7
            else:
               offsetx = 12
            # print(offsetx)

            x_time = (offsetx - time_width)
            x_date = (offscreen_canvas.width - date_width) // 2
            x_day = (offscreen_canvas.width - day_width) // 2

            graphics.DrawText(offscreen_canvas, font_date, x_day, 8, date_color, current_day)
            graphics.DrawText(offscreen_canvas, font_time, x_time, 20.5, time_color, current_time)
            graphics.DrawText(offscreen_canvas, font_time, (x_time + time_padding), 20.5, time_color, am_pm)
            graphics.DrawText(offscreen_canvas, font_date, x_date, 29, date_color, current_date)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

    def get_random_color(self):
         # random.shuffle(self.colors)
         return graphics.Color(*map(int, random.choice(self.colors).split(',')))


if __name__ == "__main__":
    digital_clock = DigitalClock()

    try:
        if not digital_clock.process():
            digital_clock.print_help()
    except KeyboardInterrupt:
        print("\nCtrl+C detected. Exiting...")
        quit()

