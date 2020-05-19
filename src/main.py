#!/usr/bin/env python
import os
import glob
import urllib
from flask import Flask
from flask import request

from urllib.parse import urlparse, unquote
from Gmail import Gmail
from epub2mobi import epub2mobi

tmp_folder = "temp/"

app = Flask(__name__)

@app.route("/", methods=['POST'])
def hello():
    if request.method == 'POST':
      email = request.form['email']
      url = request.form['url']

    if email and url:
      file_name, extension = get_file_name(url)
      book_location = f'{tmp_folder}/{file_name}{extension}'
      download_book(url, book_location)

      if extension == '.epub':
        print(f'Converting {file_name} from epub into mobi')
        book_location = book_location.replace("epub", "mobi")
        epub2mobi(tmp_folder, tmp_folder)
      elif extension != '.mobi':
        return f'File format is not epub nor mobi but {extension}'

      send_email(email, file_name, file_name, book_location)
      clean_temp()

      return f'{file_name} sent to {email}'

    return ":("


def download_book(url, file_name):
  print(f'Downloading book from {url}')
  with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
    data = response.read() # a `bytes` object
    out_file.write(data)
  print(f'Successfully downloaded book to {file_name}')


def send_email(to, subject, message, attachment):
  gmail = Gmail()
  msg = gmail.create_message_with_attachment("martriay2@gmail.com", to, subject, message, attachment)
  gmail.send_message("me", msg)


def get_file_name(url):
  url_path = urlparse(unquote(url)).path
  file_name = os.path.basename(url_path)
  name, extension = os.path.splitext(file_name)

  return name, extension

def clean_temp():
  files = glob.glob(f'{tmp_folder}/*')
  for f in files:
      os.remove(f)