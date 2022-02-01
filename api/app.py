import os
import json
import string

from flask import Flask, Response, request, abort

from dotenv import load_dotenv, find_dotenv

from newsapi import NewsApiClient

from nltk.tokenize import TreebankWordTokenizer
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import pandas as pd

import numpy as np

from database.mongodb import MongoDB

from .errors import errors

app = Flask(__name__)
app.register_blueprint(errors)

load_dotenv(find_dotenv())
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')

newsapi = NewsApiClient(api_key=NEWS_API_KEY)

connection = MongoDB.get_connection()
db = connection.newsarticles


@app.route("/allnews", methods=["GET"])
def all_news():
    page = int(request.args.get('page'))
    cursor = db.articles.find({}).skip((page-1) * 10).limit(page * 10)
    data = []

    for article in cursor:
        article['_id'] = str(article['_id'])
        data.append(article)

    return {
        "articles": data,
        "results": len(data),
    }


@app.route("/search", methods=["GET"])
def search():
    return Response("OK", status=200)


@app.route("/health")
def health():
    return Response("OK", status=200)
