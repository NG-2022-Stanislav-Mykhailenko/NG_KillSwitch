# Project: Telegram PC kill switch bot
# Author: Stanislav Mykhailenko
# License: Unlicense

# This file contains Telegram interactions

from config import *
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, filters, MessageHandler
from payload import *
import logging, googledrive
from threading import Thread

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

PASSWORD, ACTION, FORMAT, MESSAGE, FILE_MANAGER, LIST, DELETE, UPLOAD = range(8)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Enter password.")

    return PASSWORD

async def action_keyboard(update: Update):
	reply_keyboard = [["Enable input", "Disable input", "Lock screen", "Format volumes", "Play message", "File manager"]]

	await update.message.reply_text(
		"Choose your action:",
		reply_markup=ReplyKeyboardMarkup(
			reply_keyboard, one_time_keyboard=True, input_field_placeholder="Choose your action"
		),
	)

async def file_keyboard(update: Update):
	reply_keyboard = [["List files", "Upload files", "Delete files", "Go back"]]

	await update.message.reply_text(
		"Choose your action:",
		reply_markup=ReplyKeyboardMarkup(
			reply_keyboard, one_time_keyboard=True, input_field_placeholder="Choose your action"
		),
	)


async def password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	user = update.message.from_user

	if update.message.text == master_password:
		logger.info("User %s logged in.", user.first_name)
		await action_keyboard(update)

		return ACTION

	logger.info("User %s failed to log in.", user.first_name)
	await update.message.reply_text("Wrong password entered, please try again.")

	return PASSWORD

async def action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	user = update.message.from_user

	match update.message.text:
		case "Enable input":
			logger.info("Got a request from %s to enable input.", user.first_name)
			enableInput()
			await update.message.reply_text("Input enabled.", reply_markup=ReplyKeyboardRemove())
			await action_keyboard(update)
			return ACTION
		case "Disable input":
			logger.info("Got a request from %s to disable input.", user.first_name)
			disableInput()
			await update.message.reply_text("Input disabled.", reply_markup=ReplyKeyboardRemove())
			await action_keyboard(update)
			return ACTION
		case "Lock screen":
			logger.info("Got a request from %s to lock screen.", user.first_name)
			lockScreen()
			await update.message.reply_text("Screen locked.", reply_markup=ReplyKeyboardRemove())
			await action_keyboard(update)
			return ACTION
		case "Format volumes":
			logger.info("Got a request from %s to format volumes.", user.first_name)
			await update.message.reply_text("Please enter a space-separated list of the volumes you want to format.", reply_markup=ReplyKeyboardRemove())
			return FORMAT
		case "Play message":
			logger.info("Got a request from %s to play a message.", user.first_name)
			await update.message.reply_text("Please enter the message you want to play.", reply_markup=ReplyKeyboardRemove())
			return MESSAGE
		case "File manager":
			await file_keyboard(update)
			return FILE_MANAGER

async def file_manager(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	user = update.message.from_user

	match update.message.text:
		case "List files":
			logger.info("Got a request from %s to list files.", user.first_name)
			await update.message.reply_text("Please enter the path.", reply_markup=ReplyKeyboardRemove())
			return LIST
		case "Upload files":
			logger.info("Got a request from %s to upload files.", user.first_name)
			await update.message.reply_text("Please enter the path.", reply_markup=ReplyKeyboardRemove())
			return UPLOAD
		case "Delete files":
			logger.info("Got a request from %s to delete files.", user.first_name)
			await update.message.reply_text("Please enter the path.", reply_markup=ReplyKeyboardRemove())
			return DELETE
		case "Go back":
			await action_keyboard(update)
			return ACTION

async def format(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	user = update.message.from_user

	logger.info("Got a request from %s to format volumes %s.", user.first_name, update.message.text)                
	Thread(target=formatVolumes,args=(update.message.text.split(),)).start()
	await update.message.reply_text("Command to format the volumes sent.")

	await action_keyboard(update)
	return ACTION

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	user = update.message.from_user
	logger.info("Got a request from %s to play message %s.", user.first_name, update.message.text)
	Thread(target=playMessage,args=(update.message.text,)).start()
	await update.message.reply_text("Command to play the message sent.")

	await action_keyboard(update)
	return ACTION

async def list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	user = update.message.from_user

	logger.info("Got a request from %s to list files at %s.", user.first_name, update.message.text)                
	await update.message.reply_text(listData(os.path.join(update.message.text)))

	await file_keyboard(update)
	return FILE_MANAGER

async def upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	user = update.message.from_user

	logger.info("Got a request from %s to upload %s.", user.first_name, update.message.text)                
	Thread(target=uploadData,args=(os.path.join(update.message.text),)).start()
	await update.message.reply_text("Command to upload the data sent.")

	await file_keyboard(update)
	return FILE_MANAGER

async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	user = update.message.from_user

	logger.info("Got a request from %s to delete %s.", user.first_name, update.message.text)                
	Thread(target=deleteData,args=(os.path.join(update.message.text),)).start()
	await update.message.reply_text("Command to delete the data sent.")

	await file_keyboard(update)
	return FILE_MANAGER

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	user = update.message.from_user
	logger.info("User %s cancelled the conversation.", user.first_name)
	await update.message.reply_text("Request cancelled.", reply_markup=ReplyKeyboardRemove())

	return ConversationHandler.END

def startBot():
	application = Application.builder().token(token).build()
	
	conv_handler = ConversationHandler(
		entry_points=[CommandHandler("start", start)],
		states={
			PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, password)],
			ACTION: [MessageHandler(filters.Regex("^(Enable input|Disable input|Lock screen|Format volumes|Play message|File manager)$"), action)],
			FORMAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, format)],
			MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, message)],
			FILE_MANAGER: [MessageHandler(filters.Regex("^(List files|Upload files|Delete files|Go back)$"), file_manager)],
			LIST: [MessageHandler(filters.TEXT & ~filters.COMMAND, list)],
			DELETE: [MessageHandler(filters.TEXT & ~filters.COMMAND, delete)],
			UPLOAD: [MessageHandler(filters.TEXT & ~filters.COMMAND, upload)],
		},
		fallbacks=[CommandHandler("cancel", cancel)],
	)
	
	application.add_handler(conv_handler)
            
	application.run_polling()
