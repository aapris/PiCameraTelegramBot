# PiCamera Telegram Bot

`picamera_telegrambot.py` is very simple script, 
which just sends a photo to a Telegram group from attached PiCamera. 
Of course the script must be run in a Raspberry Pi.

# Installation

## PiCamera
Read [Raspberry Pi's documentation](https://www.raspberrypi.org/documentation/configuration/camera.md) 
how to install and configure PiCamera.

## Telegram bot
Read [Telegram's bot documentation](https://core.telegram.org/bots#6-botfather) 
how to create a bot and find its access token.  

## Python3
Create a Python3 virtuanenv, 
activate it and install required modules:

`pip install -r requirements.txt -U`

# Usage

You can add token as an `--token` argument or in 
`CAMBOT_TOKEN` environment variable: 

`python picamera_telegrambot.py --token 123456789:asdfghjjklqwertyuiop123456` 

or

`CAMBOT_TOKEN='123456789:asdfghjjklqwertyuiop123456' python picamera_telegrambot.py`

You can test the script without Raspberry Pi and PiCamera 
if you install Pillow module.
