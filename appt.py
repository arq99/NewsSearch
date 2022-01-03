import requests
import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask

app = Flask(__name__)

load_dotenv(find_dotenv())

NEWS_API_KEY = os.environ.get('NEWS_API_KEY')

url = (f'https://newsapi.org/v2/everything?domains=techcrunch.com,thenextweb.com&apiKey={NEWS_API_KEY}')
r = requests.get(url)

print(r.text)
