from flask import Flask, Response, request

from database.mongodb import MongoDB

from .errors import errors

app = Flask(__name__)
app.register_blueprint(errors)

connection = MongoDB.get_connection()
db = connection.newsarticles


@app.route("/all", methods=["GET"])
def all_news():
    page = int(request.args.get('page'))
    cursor = db.articles.find({}).skip((page-1) * 10).limit(10)
    data = []

    for article in cursor:
        article['_id'] = str(article['_id'])
        article.pop('article', None)
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
