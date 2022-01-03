import os
import requests

from flask import Flask, Response
from dotenv import load_dotenv, find_dotenv
from .errors import errors

app = Flask(__name__)
app.register_blueprint(errors)


@app.route("/")
def index():
    return Response("Hello, world!", status=200)


@app.route("/getnews", methods=["POST"])
def custom():
    load_dotenv(find_dotenv())
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY')

    url = f"https://newsapi.org/v2/top-headlines/sources?language=en&apiKey={NEWS_API_KEY}"
    r = requests.get(url).json()

    urls = []

    for sources in r['sources']:
        urls.append(sources['url'])

    domains = ""

    for url in urls:
        domains += f"{url[7:]},"

    url = (f"https://newsapi.org/v2/everything?"
           f"domains={domains}"
           f"&apiKey={NEWS_API_KEY}")
    r = requests.get(url).json()

    return r


@app.route("/health")
def health():
    return Response("OK", status=200)
