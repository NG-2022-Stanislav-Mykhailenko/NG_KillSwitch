# Project: Telegram PC kill switch bot
# Author: Stanislav Mykhailenko
# License: Unlicense

# This file contains the payloads

import ctypes, os, pyttsx3

def enableInput():
	ctypes.windll.user32.BlockInput(False)

def disableInput():
	ctypes.windll.user32.BlockInput(True)

def lockScreen():
	ctypes.windll.user32.LockWorkStation()

def formatVolumes(volumes):
	for volume in volumes:
		os.system('format ' + volume + ' /y')

def playMessage(message):
	engine = pyttsx3.init()
	engine.say(message)
	engine.runAndWait()
