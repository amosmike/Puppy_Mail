from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from datetime import datetime
from tqdm import tqdm
import pandas as pd
import numpy as np
import requests
import schedule
import logging
import smtplib
import random
import base64
import shutil
import scrapy
import pysftp
import time
import html
import glob
import csv
import os
import re

def get_email_password():
    with open("pass.txt", "r") as file:
        password = file.read().strip()
    return password

def get_random_image_url(query):
    api_key = "AIzaSyAFR7Swh7urS2XZ5wT8BImyFJCkUdP6-9o"
    cx = "20a296b26da3b4916"

    service = build("customsearch", "v1", developerKey=api_key)
    response = service.cse().list(q=query, cx=cx, searchType='image', num=10).execute()
    image_url = random.choice(response['items'])['link']
    return image_url

def send_email(image_url):
    print("Starting send_email")
    email_address = 'mn14m3a@gmail.com'
    email_password = get_email_password()
    recipient = 'itsmikeamos@gmail.com'

    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = recipient
    msg['Subject'] = 'Your daily cute puppy'

    text = MIMEText('Here is your daily dose of cute puppy!')
    msg.attach(text)
    print("Message attached")

    response = requests.get(image_url)
    print("Response Done")

    image = MIMEImage(response.content)
    print("Image Done")

    msg.attach(image)
    print("msg Done")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        print("Server logged in")

        server.login(email_address, email_password)
        print("Server logged in with email and password")

        server.sendmail(email_address, recipient, msg.as_string())
        print("email sent")

def download_and_open_image(image_url):
    response = requests.get(image_url, stream=True)
    local_image_filename = "puppy.jpg"
    
    # with open(local_image_filename, 'wb') as f:
    #     response.raw.decode_content = True
    #     shutil.copyfileobj(response.raw, f)

    if os.name == 'nt':  # for Windows
        os.system(f'start {local_image_filename}')
    else:  # for macOS and Linux
        os.system(f'open {local_image_filename}')

def daily_cute_puppy_email():
    query = "cute puppies"
    image_url = get_random_image_url(query)
    download_and_open_image(image_url)
    send_email(image_url)

class PuppyMail(scrapy.Spider): # "fourth_sftp_dn_scrape_reset"
    name = "puppy"

    def start_requests(self):    
        yield scrapy.Request(url='https://scrapy.org/', callback=self.parse)

    def parse(self, response):
        daily_cute_puppy_email()