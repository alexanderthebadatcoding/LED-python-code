import time
import datetime
from PIL import Image, ImageDraw, ImageFont
from rgbmatrix import RGBMatrix, RGBMatrixOptions

# Set up the RGB LED matrix
options = RGBMatrixOptions()
options.hardware_mapping = "adafruit-hat-pwm"  # Check your hardware mapping
matrix = RGBMatrix(options=options)

# Create an image buffer and drawing context
image = Image.new("RGB", (matrix.width, matrix.height))
draw = ImageDraw.Draw(image)

# Load a font (change the path to the font file as needed)
font = ImageFont.truetype("fonts/score_large.otf", size=16)

while True:
    current_time = datetime.datetime.now().time()
    formatted_time = current_time.strftime("%H:%M:%S")

    # Text to display
    text = formatted_time

    # Clear the matrix
    matrix.Clear()

    # Draw the text on the image
    draw.text((1, 1), text, fill=(255, 205, 255), font=font)

    # Convert the image to RGB565 format
    rgb565_image = image.convert("RGB")

    # Display the image on the matrix
    matrix.SetImage(rgb565_image)

    # Delay for a while (e.g., 5 seconds)
    time.sleep(5)
