#pip install RPi.GPIO

import RPi.GPIO as GPIO
import subprocess
import time

# Define GPIO pins
BUTTON_PIN = 17  # Change this to the actual GPIO pin you're using

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to run the selected script
def run_script(script_file):
    subprocess.run(["python", script_file])

try:
    script_running = None

    while True:
        # Check if the button is pressed
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            if script_running is None or script_running == 'script2.py':
                # Switch to script1
                if script_running:
                    script_running = None
                else:
                    script_running = 'script1.py'
                run_script('script1.py')

            elif script_running == 'script1.py':
                # Switch to script2
                script_running = 'script2.py'
                run_script('script2.py')

        time.sleep(0.1)  # Add a small delay to debounce the button

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
