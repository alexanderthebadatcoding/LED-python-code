# Example Python Scripts for Raspberry Pi with the LED-Matrix

Trying to learn python and better understand how to use the pi Matrix. Based partially on [mikemountain/nfl-led-scoreboard](https://github.com/mikemountain/nfl-led-scoreboard)

_some Chat-GPT code_

## Installation

This project relies on standard Python libraries, and you don't need to install any external dependencies. The `time` module, which is used for time-related operations, is included in the Python standard library, so there's no need to install it separately.

```
sudo apt-get update
sudo apt-get install git python-pip
```

This installation process might take some time because it will install all the dependencies listed below.

```
git clone --recursive https://github.com/alexanderthebadatcoding/raspi-py/
cd raspi-py/
sudo chmod +x install.sh
sudo ./install.sh
```

[rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/bindings/python#building): The open-source library that allows the Raspberry Pi to render on the LED matrix.

[requests](https://requests.kennethreitz.org/en/master/): To call the API and manipulate the received data.

For more information about the `rpi-rgb-led-matrix` library, including detailed documentation and configuration options, please visit the [rpi-rgb-led-matrix repository](https://github.com/hzeller/rpi-rgb-led-matrix).

**Make sure to change the API key in weather**
