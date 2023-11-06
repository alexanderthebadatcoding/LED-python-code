#!/usr/bin/env python

from samplebase import SampleBase
from rgbmatrix import graphics
import random
from pyowm import OWM
from pyowm.utils import timestamps

owm = OWM('API_key')
mgr = owm.weather_manager()
observation = mgr.weather_at_place("Kansas City,US")
w = observation.weather


class WeatherDisplay(SampleBase):
    def __init__(self, *args, **kwargs):
        super(WeatherDisplay, self).__init__(*args, **kwargs)
        self.parser.add_argument("-f_text", "--font_text", help="Path to font file for date (BDF format)", default="/home/gilby/fonts/4x6.bdf")
        self.parser.add_argument("-f_temp", "--font_temp", help="Path to font file for date (BDF format)", default="/home/gilby/fonts/luBS12.bdf")
        self.parser.add_argument("--led-pwm-lsb-nanoseconds=250")

    def get_weather_data(self):
        try:
            temperature_fahrenheit = w.temperature('fahrenheit')['temp']
            temperature_text = f"{temperature_fahrenheit:.0f}°F"

            if temperature_fahrenheit < 50:
                 temperature_color = graphics.Color(37, 124, 163)  # Icy Blue
            elif 50 <= temperature_fahrenheit <= 60:
                   temperature_color = graphics.Color(0, 176, 255)  # Blueish
            elif 60 <= temperature_fahrenheit <= 70:
                   temperature_color = graphics.Color(124, 255, 121)  # Greenish
            elif 70 <= temperature_fahrenheit <= 80:
                   temperature_color = graphics.Color(255, 196, 0)  # Orange
            elif temperature_fahrenheit > 80:
                   temperature_color = graphics.Color(252, 87, 78)  # Redish
            else:
                 temperature_color = graphics.Color(255, 255, 255)  # White

            return temperature_text, temperature_color
            time.sleep(30.0)
        except Exception as e:
            return "Error fetching data"

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font_text = graphics.Font()
        font_text.LoadFont(self.args.font_text)
        font_temp = graphics.Font()
        font_temp.LoadFont(self.args.font_temp)
        date_color = graphics.Color(255, 255, 255)
        print(len(w.detailed_status))
        if len(w.detailed_status) > 15:
           offset = 2
        elif len(w.detailed_status) > 14:
           offset = 3
        elif len(w.detailed_status) > 10:
           offset = 4
        else:
           offset = 15
           # print(len(w.detailed_status))


        while True:
            offscreen_canvas.Clear()

            # Display weather data
            weather_text, weather_color = self.get_weather_data()
            # graphics.DrawText(offscreen_canvas, font_text, 12, 7, date_color, "Today:")
            graphics.DrawText(offscreen_canvas, font_temp, 16, 18, weather_color, weather_text)
            graphics.DrawText(offscreen_canvas, font_text, offset, 28, date_color, w.detailed_status)

            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


if __name__ == "__main__" :
    weather_display = WeatherDisplay()
    if not weather_display.process():
        weather_display.print_help()
