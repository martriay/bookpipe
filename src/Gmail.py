#!/usr/bin/env python
from __future__ import print_function
import pickle
import os.path
import mimetypes
import base64

from apiclient import errors, discovery
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase


class Gmail():
  SCOPES = ['https://www.googleapis.com/auth/gmail.send']
  service = None

  def __init__(self):
    self.authenticate()
  
  
  def authenticate(self):
    creds = None
    if os.path.exists('token.pickle'):
      with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
        creds = flow.run_local_server(port=0)

      with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

    self.service = build('gmail', 'v1', credentials=creds)


  def create_message(self, sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


  def create_message_with_attachment(self, sender, to, subject, message_text, file):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    content_type, encoding = mimetypes.guess_type(file)

    if content_type is None or encoding is not None:
      content_type = 'application/octet-stream'

    main_type, sub_type = content_type.split('/', 1)

    if main_type == 'text':
      fp = open(file, 'r')
      msg = MIMEText(fp.read(), _subtype=sub_type)
      fp.close()
    elif main_type == 'image':
      fp = open(file, 'rb')
      msg = MIMEImage(fp.read(), _subtype=sub_type)
      fp.close()
    elif main_type == 'audio':
      fp = open(file, 'rb')
      msg = MIMEAudio(fp.read(), _subtype=sub_type)
      fp.close()
    elif main_type == 'application':
      fp = open(file, 'rb')
      msg = MIMEApplication(fp.read(), _subtype=sub_type)
      fp.close()
    else:
      fp = open(file, 'rb')
      msg = MIMEBase(main_type, sub_type)
      msg.set_payload(fp.read())
      fp.close()

    filename = os.path.basename(file)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


  def send_message(self, user_id, message):
    try:
      message = (self.service.users().messages().send(userId=user_id, body=message).execute())
      print('Sent message Id: %s' % message['id'])
      return message
    except(errors.HttpError, error):
      print('An error occurred: %s' % error)