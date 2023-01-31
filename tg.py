# Project: Telegram PC kill switch bot
# Author: Stanislav Mykhailenko
# License: Unlicense

# This file contains Telegram interactions

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, filters, MessageHandler
from payload import *
import logging
from threading import Thread

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

ACTION, FORMAT, MESSAGE = range(3)

def getToken():
	with open(os.path.realpath(os.path.dirname(__file__)) + '/' + 'token.txt', 'r') as file:
		return file.read()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Enable input", "Disable input", "Lock screen", "Format volumes", "Play message"]]

    await update.message.reply_text(
        "Choose your action:",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Choose your action"
        ),
    )

    return ACTION

async def action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	user = update.message.from_user

	match update.message.text:
		case "Enable input":
			logger.info("Got a request from %s to enable input.", user.first_name)
			enableInput()
			await update.message.reply_text("Input enabled.", reply_markup=ReplyKeyboardRemove())
			return ConversationHandler.END
		case "Disable input":
			logger.info("Got a request from %s to disable input.", user.first_name)
			disableInput()
			await update.message.reply_text("Input disabled.", reply_markup=ReplyKeyboardRemove())
			return ConversationHandler.END
		case "Lock screen":
			logger.info("Got a request from %s to lock screen.", user.first_name)
			lockScreen()
			await update.message.reply_text("Screen locked.", reply_markup=ReplyKeyboardRemove())
			return ConversationHandler.END
		case "Format volumes":
			logger.info("Got a request from %s to format volumes.", user.first_name)
			await update.message.reply_text("Please type a space-separated list of the volumes you want to format.", reply_markup=ReplyKeyboardRemove())
			return FORMAT
		case "Play message":
			logger.info("Got a request from %s to play a message.", user.first_name)
			await update.message.reply_text("Please type the message you want to play.", reply_markup=ReplyKeyboardRemove())
			return MESSAGE

async def format(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	user = update.message.from_user

	logger.info("Got a request from %s to format volumes %s.", user.first_name, update.message.text)                
	Thread(target=formatVolumes,args=(update.message.text.split(),)).start()
	await update.message.reply_text("Command to format the volumes sent.")

	return ConversationHandler.END

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	user = update.message.from_user
	logger.info("Got a request from %s to play message %s.", user.first_name, update.message.text)
	Thread(target=playMessage,args=(update.message.text,)).start()
	await update.message.reply_text("Command to play the message sent.")

	return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	user = update.message.from_user
	logger.info("User %s canceled the conversation.", user.first_name)
	await update.message.reply_text("Request cancelled.", reply_markup=ReplyKeyboardRemove())

	return ConversationHandler.END

def startBot():
	application = Application.builder().token(getToken()).build()
	
	conv_handler = ConversationHandler(
		entry_points=[CommandHandler("start", start)],
		states={
			ACTION: [MessageHandler(filters.Regex("^(Enable input|Disable input|Lock screen|Format volumes|Play message)$"), action)],
			FORMAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, format)],
			MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, message)],
		},
		fallbacks=[CommandHandler("cancel", cancel)],
	)
	
	application.add_handler(conv_handler)
            
	application.run_polling()
