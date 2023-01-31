# Computer kill switch

This program is a PC kill switch Telegram bot. It is a project for New Generation.

## Features
- disabling and re-enabling keyboard and mouse input
- locking the screen
- formatting partitions
- playing text-to-speech messages

## Limitations
- input lock resets if Control-Alt-Delete is pressed
- volumes used by some software at the time of request cannot be formatted
- works on Windows only

## Usage
Before starting the bot, copy config-example.py file to config.py and put the password and the token. Administrator privileges are required so that the bot is able to disable input and format partitions. Once the bot is started, send /start to its account on Telegram and enter the password to see what can be done.

## Licensing
All code in this repository is Unlicensed, see UNLICENSE.
