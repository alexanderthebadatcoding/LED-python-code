import time
import argparse
import sys
import os
from samplebase import SampleBase
from rgbmatrix import graphics

class ClockDisplay(SampleBase):
    def run(self):
        canvas = self.matrix.CreateFrameCanvas()

        font = graphics.Font()
        font.LoadFont("../../../fonts/6x9.bdf")

        textColor = graphics.Color(255, 255, 255)

        while True:
            canvas.Clear()
            graphics.DrawText(canvas, font, 0, 7, textColor, time.strftime("%H:%M:%S"), True)
            canvas = self.matrix.SwapOnVSync(canvas)
            time.sleep(1)


