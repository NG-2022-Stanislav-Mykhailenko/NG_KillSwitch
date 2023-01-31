# Computer kill switch

This program is a PC kill switch Telegram bot. It is a project for New Generation.

## Security notice
This program provides no access control, so anyone knowing the bot username is able to use it.

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
Before starting the bot, its token must be put into token.txt file with no newlines. Administrator privileges are required so that the bot is able to disable input and format partitions. Once the bot is started, send /start to its account on Telegram to see what can be done.

## Licensing
All code in this repository is Unlicensed, see UNLICENSE.
