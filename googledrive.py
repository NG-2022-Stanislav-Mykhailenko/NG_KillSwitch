# Project: Telegram PC kill switch bot
# Author: Stanislav Mykhailenko
# License: Unlicense

# This file contains Google Drive interactions


from __future__ import print_function

import os
from mimetypes import MimeTypes
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


creds = None

def authenticate():
	global creds
	# The file token.json stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists(os.path.join(os.path.dirname(__file__), 'token.json')):
		creds = Credentials.from_authorized_user_file(os.path.join(os.path.dirname(__file__), 'token.json'), ['https://www.googleapis.com/auth/drive'])
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				os.path.join(os.path.dirname(__file__), 'credentials.json'), ['https://www.googleapis.com/auth/drive'])
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open(os.path.join(os.path.dirname(__file__), 'token.json'), 'w') as token:
			token.write(creds.to_json())



def createFolder(name, parent):
	try:
		service = build('drive', 'v3', credentials=creds)
		file_metadata = {
			'name': [name],
			'mimeType': 'application/vnd.google-apps.folder',
			'parents': [parent]
		}

		file = service.files().create(body=file_metadata, fields='id'
                                      ).execute()
		return file.get('id')

	except HttpError as error:
		print(F'An error occurred: {error}')
		return None


def uploadFile(path, folder):
	try:
		service = build('drive', 'v3', credentials=creds)

		name = os.path.basename(os.path.normpath(path))

		file_metadata = {
			'name': [name],
			'parents': [folder]
		}

		mimetype = MimeTypes().guess_type(path)[0]

		media = MediaFileUpload(path,
				mimetype=mimetype)

		file = service.files().create(body=file_metadata, media_body=media,
				fields='id').execute()
		return file.get('id')

	except HttpError as error:
		print(F'An error occurred: {error}')
		file = None
