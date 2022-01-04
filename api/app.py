import os
import requests

from flask import Flask, Response, request
from dotenv import load_dotenv, find_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .errors import errors

app = Flask(__name__)
app.register_blueprint(errors)


def getnewsarticles():
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
           f"&apiKey={NEWS_API_KEY}"
           f"&pageSize=100")
    articles = requests.get(url).json()

    return articles


def tokenize_and_stem(s):
    STEMMER = PorterStemmer()
    TOKENIZER = TreebankWordTokenizer()
    REMOVE_PUNCTUATION_TABLE = str.maketrans({x: None for x in string.punctuation})

    return [STEMMER.stem(t) for t
            in TOKENIZER.tokenize(s.translate(REMOVE_PUNCTUATION_TABLE))]


@app.route("/allnews", methods=["GET"])
def allnews():
    return Response(getnewsarticles(), 200)


@app.route("/search", methods=["POST"])
def search():
    query = request.args.get('query')
    articles = getnewsarticles()['articles']

    docs = []

    for article in articles:
        docs.append(article['description'])

    vectorizer = TfidfVectorizer(tokenizer=tokenize_and_stem, stop_words='english')

    vectorizer.fit(docs)

    query_vector = vectorizer.transform([query]).todense()

    doc_vectors = vectorizer.transform(docs)
    similarity = cosine_similarity(query_vector, doc_vectors)

    ranks = (-similarity).argsort(axis=None)

    relevant_searches = []

    for i in range(10):
        relevant_searches.append(docs[ranks[i]])

    return Response(relevant_searches, 200)


@app.route("/health")
def health():
    return Response("OK", status=200)
