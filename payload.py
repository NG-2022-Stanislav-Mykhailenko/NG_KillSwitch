# Project: Telegram PC kill switch bot
# Author: Stanislav Mykhailenko
# License: Unlicense

# This file contains the payloads

from googledrive import *
from config import *
import ctypes, os, pyttsx3, shutil

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

def listData(path):
	try:
		return os.listdir(path)
	except NotADirectoryError:
		return "Is a file."
	except FileNotFoundError:
		return "File or directory not found."
	except:
		return "An error occurred when trying to access the data."

def uploadFolder(path, parentDirectory):
	directory = createFolder(os.path.basename(os.path.normpath(path)), parentDirectory)
	entries = os.listdir(path)
	for entry in entries:
		if os.path.isdir(os.path.join(path, entry)):
			uploadFolder(os.path.join(path, entry), directory)
		else:
			uploadFile(os.path.join(path, entry), directory)

def uploadData(path):
	if not os.path.exists(path):
		return False
	if os.path.isdir(path):
		uploadFolder(path, root_folder)
	else:
		uploadFile(path, root_folder)

def deleteData(path):
	shutil.rmtree(path, ignore_errors=True)
