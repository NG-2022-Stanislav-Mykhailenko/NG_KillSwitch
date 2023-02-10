# Computer kill switch

This program is a PC kill switch Telegram bot. It is a project for New Generation.

## Features
- disabling and re-enabling keyboard and mouse input
- locking the screen
- formatting partitions
- executing commands
- playing text-to-speech messages
- listing directories, deleting directories and files, uploading them to Google Drive, and sending them to the machine

## Limitations
- input lock resets if Control-Alt-Delete is pressed
- volumes used by some software at the time of request cannot be formatted
- works on Windows only

## Usage
In order to run the bot, you need a Telegram bot token and Google Drive API credentials. A directory on Google Drive where the bot put its files should also be created.

Before starting the bot, copy config-example.py file to config.py and put the Telegram bot token, the bot protection password and the Google Drive folder ID. Put your Google API credentials into credentials.json file. Administrator privileges are required so that the bot is able to disable input and format partitions. Once the bot is started, send /start to its account on Telegram and enter the password to see what can be done.

## Licensing
All code in this repository is Unlicensed, see UNLICENSE.
